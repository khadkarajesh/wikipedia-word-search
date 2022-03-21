import smtplib
import ssl
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import environ

MAIL_PORT = "mail_port"
MAIL_PASSWORD = "mail_password"
SENDER_EMAIL = "sender_email"
RECEIVER_EMAIL = "receiver_email"
SMTP = "smtp"

NOTIFICATION_MESSAGE = "Alert! words exceeded the threshold. Take corrective action ahead of time"
EMAIL_SUBJECT = "Word Threshold Exceeded"


class Notifier(ABC):
    @abstractmethod
    def notify(self):
        pass


class NotificationChannelType:
    EMAIL = "email"
    SMS = "sms"
    PUSH_NOTIFICATION = "push"
    ALL = [EMAIL, SMS, PUSH_NOTIFICATION]


class NotifierFactory:
    def __init__(self):
        self._notifier = {}

    def register(self, channel_type, notifier):
        self._notifier[channel_type] = notifier

    def get(self, channel_type):
        notifier = self._notifier.get(channel_type)
        if not channel_type or channel_type not in NotificationChannelType.ALL:
            raise ValueError(channel_type)
        return notifier()


env = environ.Env()


class EmailNotifier(Notifier):
    def notify(self):
        port = env('MAIL_PORT')
        password = env('MAIL_PASSWORD')
        smtp_server = env('SMTP')

        sender_email = env('SENDER_EMAIL')
        receiver_email = env('RECEIVER_EMAIL')

        message = MIMEMultipart("alternative")
        message["Subject"] = EMAIL_SUBJECT
        message['From'] = sender_email
        message['To'] = receiver_email

        email_body = MIMEText(NOTIFICATION_MESSAGE, "plain")
        message.attach(email_body)

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            try:
                server.starttls(context=context)
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                print(f"exception while sending email {e}")


class SMSNotifier(Notifier):
    def notify(self):
        pass


class GCMNotifier(Notifier):
    def notify(self):
        pass


factory = NotifierFactory()
factory.register(NotificationChannelType.EMAIL, EmailNotifier)
email_notifier = factory.get(NotificationChannelType.EMAIL)
