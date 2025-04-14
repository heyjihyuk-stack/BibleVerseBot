from flask import Flask, jsonify
import requests

app = Flask(__name__)

# 성경 본문을 가져오는 API 엔드포인트
@app.route('/verse', methods=['GET'])
def get_verse():
    url = "https://sum.su.or.kr:8888/bible/today/1000"  # 성경 본문을 가져오는 URL
    response = requests.get(url)  # 해당 URL로 HTTP GET 요청 보내기
    
    if response.status_code == 200:  # 성공적으로 데이터를 받았을 때
        return jsonify({"verse": response.json()})  # JSON 형식으로 반환
    else:
        return jsonify({"error": "Failed to retrieve Bible verse"}), 500  # 오류 처리

if __name__ == '__main__':
    app.run(debug=True)  # 개발 모드로 서버 실행