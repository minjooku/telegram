import requests
from decouple import config

#api 요청 기본사항
url='https://api.telegram.org'
token=config('TELEGRAM_BOT_TOKEN')
#봇과 대화하고 있는 사용자 CHAT_ID 추출
chat_id=config('CHAT_ID')

# chat_id=requests.get(f'{url}/bot{token}/getUpdates').json()['result'][0]['message']['from']['id']


text=input('메세지를 입력하세요: ')

send_message=requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')


print(send_message.text)