from concurrent.futures import ThreadPoolExecutor
import requests
from flask_mail import Mail, Message
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=4))
s.mount('https://', HTTPAdapter(max_retries=4))


class MailServer:
    def __init__(self):
        self.executor = ThreadPoolExecutor(32)
        self.app = None
        self.mail = Mail()

    def init_app(self, app):
        self.app = app
        self.mail.init_app(app)
        print("MailServer init_app")

    def send_async_email(self, mail_to, subject, content):
        with self.app.app_context():
            msg = Message(subject, recipients=[mail_to])
            msg.body = content
            self.mail.send(msg)

    def sendMail(self, mail_to, subject, content):
        self.executor.submit(self.send_async_email, mail_to, subject, content)

    def sendListMail(self, mailList, subject, content):
        for mail_to in mailList:
            self.executor.submit(self.send_async_email, mail_to, subject, content)
