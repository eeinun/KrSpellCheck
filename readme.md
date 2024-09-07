### 네이버 맞춤법 검사기

### 예시
```python
from SpellCheckAgent import Agent


agent = Agent()
wrong_sentence = "산지 세달은 다돼가는 화롯대에는 감자를 깊숙히 넣을 수 있어."
raw, mod, err = agent.requestSpellCheck(wrong_sentence)
print(f"맞춤법 오류 {err}개 있음")
raw.display()
mod.display()
```