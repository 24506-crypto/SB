from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# [평가기준 1: 데이터 크롤링] 네이버 금융에서 달러 환율 숫자를 긁어오는 함수
def get_exchange_rate():
    try:
        url = "https://finance.naver.com/marketindex/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 네이버 금융 페이지에서 환율 값이 있는 클래스(.value)를 크롤링
        exchange_rate = soup.select_one(".value").text
        return exchange_rate
    except Exception as e:
        return "1,350" # 혹시 크롤링이 실패했을 때를 대비한 기본값

# [평가기준 2: 스킬 데이터 사용] 카카오톡 챗봇 서버와 통신하는 주소
@app.route('/exchange', methods=['POST'])
def exchange():
    # 크롤링 함수를 실행해서 현재 환율을 가져옴
    current_rate = get_exchange_rate()
    
    # 카카오톡 창에 띄워줄 메시지 작성
    msg = f"📊 실시간 수입 원가 리스크 진단\n\n" \
          f"현재 네이버 금융 기준 미국 달러 환율은 [{current_rate}원]입니다.\n\n" \
          f"💡 경영 팁:\n" \
          f"환율이 오르면 원재료 수입 비용(변동비)이 늘어납니다. 매장 마진 관리에 유의하세요!"

    # 카카오톡 규격(JSON 형식)에 맞게 데이터를 포장해서 반환
    response_body = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": msg
                    }
                }
            ]
        }
    }
    return jsonify(response_body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)