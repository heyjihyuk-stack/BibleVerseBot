from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['POST'])
def kakao_webhook():
    # 1. 성경 본문 가져오기
    url = "https://sum.su.or.kr:8888/bible/today/1000"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    bible_text = soup.select_one('.bible_text').get_text(strip=True)
    bible_info = soup.select_one('.bibleinfo_box').get_text(strip=True)

    # 2. 카카오 오픈빌더 응답 형식 맞춰서 리턴
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": f"{bible_info}\n\n{bible_text}"
                    }
                }
            ]
        }
    })