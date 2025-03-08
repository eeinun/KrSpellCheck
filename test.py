import re
import json
import requests


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
doc = requests.get(
    "https://search.naver.com/search.naver?query=%EB%A7%9E%EC%B6%A4%EB%B2%95%EA%B2%80%EC%82%AC%EA%B8%B0",
    headers=headers
)
pk = re.search(r"passportKey=[0-9a-f]*", str(doc.content)).group()
query = "설량한 사람이 화롯대 속 몽땅연필을 바라만본다."
spchk = requests.get(
    f"https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy?{pk}&q={query}&where=nexearch&color_blindness=0",
    headers=headers
)
res = json.loads(spchk.text)
print(res)
print((spchk.text))

# import SpellCheckAgent
#
#
# agent = SpellCheckAgent.Agent()
# print(agent.requestSpellCheck("설량한 사람이 화롯대 속 몽땅연필을 바라만본다.", as_string=True))
#
# from SpellCheckAgent import Sentence
#
#
# sc = Sentence("<em class='blue_text'>선량한</em> 사람이 <em class='violet_text'>화롯대</em> 속 <em class='red_text'>몽당연필을</em> <em class='green_text'>바라만 본다.</em>")