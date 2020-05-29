from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)

messages = [
    {'username':'Name1', 'text': 'Hello', 'time':time.time()},
{'username':'Name2', 'text': 'Hi', 'time':time.time()}
]

users = {
    'Jack': '123456',
    'Mary': '123123',
}

@app.route("/")
def hello():
    return "Hello to Python messenger!"


@app.route("/status")
def status_view():
    return {
        'time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'status': True,
        'messages_count': len(messages),
        'users_count': len(users)
    }

@app.route("/messages")
def messages_view():
    '''
    input: after
    output: {
        'messages': [
        'username': str, 'text': str, 'time': float],
        ...
    }
    '''

    after = float(request.args['after'])

    new_messages = [message for message in messages if message['time'] > after]
    return {'messages': new_messages}

@app.route("/send", methods = ['POST'])
def send_view():
    '''
    input: {
    'username': str
    'text': str
    output:  {'ok': True}


    '''
    data = request.json
    username = data['username']
    password = data['password']

    if username not in users or users[username] != password:
        return {'ok': False}


    text = data['text']

    messages.append({'username': username, 'text': text, 'time':time.time()})
    return {'ok': True}


@app.route("/auth", methods = ['POST'])
def auth_view():
    data = request.json
    username = data['username']
    password = data['password']

    if username not in users:
        users[username] = password
        return {'ok': True}
    elif users[username] == password:
        return {'ok': True}
    else:
        return {'ok': False}


def main():
    app.run()

if __name__ == '__main__':
    main()