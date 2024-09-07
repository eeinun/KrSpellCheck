import time
import requests
import json
import re


class TextToken:
    color_map = {
        "red": "ff7961",
        "green": "76e889",
        "blue": "709bff",
        "violet": "bc82ff"
    }
    @staticmethod
    def deco(text, color="000000", b=False, i=False, u=False):
        additional = ""
        if b:
            additional += "1;"
        if i:
            additional += "3;"
        if u:
            additional += "4;"
        pre = f"\033[{additional}38;2;{int(color[:2], base=16)};{int(color[2:4], base=16)};{int(color[4:], base=16)}m"
        post = "\033[0m"
        return pre + text + post

    def __init__(self, value, color="000000", b=False, i=False, u=False):
        self.value = value
        self.color = color
        self.underline = u
        self.ANSI_format = TextToken.deco(self.value, color, b=b, i=i, u=u)

    def __str__(self):
        return self.value

    def to_console(self):
        return self.ANSI_format

    def to_html(self):
        return f"""<span color="#{self.color}">{self.value}</span>"""


class Sentence:
    def __init__(self, html: str):
        self.tokenized = None
        self.parser(html)

    def parser(self, html: str):
        tokens = list()
        v, c, u, opened = "", "000000", False, False
        for i, j in re.findall(r"(<[^>]+>)|([^<]*)", html):
            tkn = i if len(i) else j
            if len(tkn) == 0:
                continue
            if tkn[0] == '<' and tkn[1] == '/':
                tokens.append(TextToken(v, color=c, u=u))
                v, c, u, opened = "", "000000", False, False
            elif tkn[0] == '<':
                opened = True
                attr = re.search(r"'([a-zA-Z_]+)'", tkn)
                if attr is None:
                    continue
                elif attr.group()[1:-1] == "result_underline":
                    u = True
                elif attr.group()[-5:-1] == "text":
                    c = TextToken.color_map[attr.group().split('_')[0][1:]]
            elif not opened:
                tokens.append(TextToken(tkn))
            else:
                v += tkn
        self.tokenized = tokens[:]
        
    def __str__(self):
        return ''.join([str(x) for x in self.tokenized])

    def display(self):
        print(''.join([x.to_console() for x in self.tokenized]))

    def html_output(self):
        print(f"<div>{''.join([x.to_html() for x in self.tokenized])}<div>")


class Agent:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    pk_url = "https://search.naver.com/search.naver?query=맞춤법계산기"
    chk_url = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"
    def __init__(self):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if data['passportKey']['lifetime'] < time.time():
            data['passportKey']['value'] = self.getPassportKey()
            data['passportKey']['lifetime'] = ((time.time() + 32400) // 86400 + 1) * 86400 - 32400
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
        self.passportKey = data['passportKey']['value']

    def getPassportKey(self):
        doc = requests.get(
            Agent.pk_url,
            headers=Agent.headers
        )
        return re.search(r"passportKey=[0-9a-f]*", str(doc.content)).group().split('=')[-1]

    def requestSpellCheck(self, sentence, as_string=False):
        if len(sentence) > 300:
            print("글자 수는 300자를 넘을 수 없습니다.")
            return None, None
        res = requests.get(
            Agent.chk_url + f"?passportKey={self.passportKey}&q={sentence}&where=nexearch&color_blindness=0",
            headers=Agent.headers
        )
        content = json.loads(res.text)
        errcnt = content["message"]["result"]["errata_count"]
        if errcnt == 0:
            return Sentence(sentence), Sentence(sentence), 0
        if as_string:
            return content["message"]["result"]["notag_html"]
        return Sentence(content["message"]["result"]["origin_html"]), Sentence(content["message"]["result"]["html"]), errcnt

    def processParagraph(self, paragraph):
        pass


if __name__ == "__main__":
    agent = Agent()
    wrong_sentence = "산지 세달은 다돼가는 화롯대에는 감자를 깊숙히 넣을 수 있어."
    raw, mod, err = agent.requestSpellCheck(wrong_sentence)
    print(f"맞춤법 오류 {err}개 있음")
    raw.display()
    mod.display()