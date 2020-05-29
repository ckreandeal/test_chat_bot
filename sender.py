import requests

# {'username':'Name1', 'text': 'Hello', 'time':time.time()}



res = requests.get('http://127.0.0.1:5000/status')
print(res.text)

print("Enter your name")
username = input()

print("Enter your pass")
password = input()

res = requests.post('http://127.0.0.1:5000/auth', json={'username': username, 'password':password})

if not res.json()['ok']:
    print('incorrect pass')
    exit()

while True:
    print("Your message")
    text = input()
    res = requests.post('http://127.0.0.1:5000/send', json={'username': username,'password': password, 'text': text,})
    print()

