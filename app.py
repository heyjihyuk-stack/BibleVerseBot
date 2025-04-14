from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["POST"])
def kakao_webhook():
    # 성경본문 페이지 요청
    url = "https://sum.su.or.kr:8888/bible/today/1000"
    response = requests.get(url)
    response.encoding = 'utf-8'  # 한글 깨짐 방지

    # 파싱 시작
    soup = BeautifulSoup(response.text, 'html.parser')

    # 시작 div부터 종료 div까지 텍스트 추출
    start_div = soup.find("div", {"id": "dailybible_info"})
    end_div = soup.find("div", {"id": "audio_href"})

    # 텍스트들을 담을 리스트
    bible_texts = []

    # 현재 div부터 시작해서 다음 형제 요소들 순회
    current = start_div
    while current and current != end_div:
        if current.name == "div":
            bible_texts.append(current.get_text(strip=True))
        current = current.find_next_sibling()

    # 마지막 div도 포함
    if end_div:
        bible_texts.append(end_div.get_text(strip=True))

    # 전체 본문 합치기
    full_text = "\n".join(bible_texts)

    # 카카오 응답
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": full_text
                    }
                }
            ]
        }
    })