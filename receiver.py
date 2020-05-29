import requests
import time
from datetime import datetime


last_time = 0
while True:
    res = requests.get('http://127.0.0.1:5000/messages', params={'after': last_time})

    messages = res.json()['messages']

    for message in messages:
        beauty_time = datetime.fromtimestamp(message['time'])
        beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
        print(message['username'], beauty_time)
        print(message['text'],)
        print()

        last_time = message['time']

    time.sleep(1)