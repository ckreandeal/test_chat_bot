import threading
from datetime import datetime
import time

import PyQt5
from server import main
import requests

from PyQt5 import QtWidgets

import chat_ui


class ExampleApp(QtWidgets.QMainWindow, chat_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_click)
        self.mutex = threading.Lock()
        thread = threading.Thread(target=self.update_messages)
        thread.start()

    def sed_message(self, username, password, text):
        res = requests.post('http://127.0.0.1:5000/auth', json={'username': username, 'password': password})

        if not res.json()['ok']:
            self.add_to_chat('Can not send message')
            return

        res = requests.post('http://127.0.0.1:5000/send',
                            json={'username': username, 'password': password, 'text': text, })
        if not res.json()['ok']:
            self.add_to_chat('Can not send message')

    def button_click(self):
        try:

            self.sed_message(
                self.textEdit_2.toPlainText(),
                self.textEdit_3.toPlainText(),
                self.textEdit.toPlainText(),
            )
        except:
            pass
        self.mutex.acquire()
        self.textEdit.setText('')
        self.textEdit.repaint()
        self.mutex.release()

    def add_to_chat(self, text):
        self.mutex.acquire()
        self.textBrowser.append(text)
        # self.textBrowser.repaint()
        self.mutex.release()

    def update_messages(self):
        last_time = 0
        while True:
            try:
                res = requests.get('http://127.0.0.1:5000/messages', params={'after': last_time})

                messages = res.json()['messages']

                for message in messages:
                    beauty_time = datetime.fromtimestamp(message['time'])
                    beauty_time = beauty_time.strftime('%d/%m/%Y %H:%M:%S')
                    self.add_to_chat(message['username'] + '' + beauty_time)
                    self.add_to_chat(message['text'], )
                    self.add_to_chat('')

                    last_time = message['time']
            except:
                self.add_to_chat('Can not receive messages')

            time.sleep(1)


# main()

app = QtWidgets.QApplication([])
window = ExampleApp()
window_2 = ExampleApp()
window.show()
window_2.show()
app.exec_()
