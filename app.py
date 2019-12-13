from flask import Flask, render_template,request
from decouple import config
import requests, pprint,random, html

app = Flask(__name__)
#Telegram API
url='https://api.telegram.org'
token=config('TELEGRAM_BOT_TOKEN')
chat_id=config('CHAT_ID')

#google API
google_url = 'https://translation.googleapis.com/language/translate/v2'
google_key= config('GOOGLE_TOKEN')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route(f'/{token}', methods=['POST'])
def telegram():
    # 1. 텔레그램이 보내주는 데이터 구조확인
    # pprint.pprint(request.get_json())
    # 2. 사용자아이디, 메시지 추출
    chat_id = request.get_json().get('message').get('chat').get('id')
    message = request.get_json().get('message').get('text')
 # # 3.텔레그램을 API에 요청해서 답장 보내주기
    # requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')
    # return '',200
    #사용자가 로또라고 입력하면 로또 번호 6개 불러주기
    if message == '로또':
        result=random.sample(range(1,46),6)
    elif message[:4] =='/번역 ':
        data={
            'q':message[4:],
            'source':'ko',
            'target':'en'

        }
        reponse=requests.post(f'{google_url}?key={google_key}',data).json()
        result=html.unescape(reponse['data']['translations'][0]['translatedText'])
    #그 외의 경우엔 메아리
    else:
        result =message

    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={result}')
    return '',200


   




@app.route('/write')
def write():
    return render_template('write.html')


@app.route('/send')
def send():
    # 1. 사용자가 입력한 데이터 바당오기
    text=request.args.get('message')   
    # 2. 텔레그램 API 메시지 전송요청 보내기 
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return "전송완료"
   


#반드시 파일 최하단에 위치시킬 것.
if __name__=='__main__':
    app.run(debug=True)