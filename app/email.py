from flask_mail import Message
from app import mail

def send_mail(subject, sender, recipients, text_body, html_body=None, attachments:list=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body is not None:
        msg.html = html_body
    if attachments is not None:
        for byte in attachments:
            msg.attach("image.png", "image/png", byte)
    mail.send(msg)