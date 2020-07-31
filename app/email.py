from flask_mail import Message
from app import app, mail
import threading

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print("sent")

def send_mail(subject, sender, recipients, text_body, html_body=None, attachments:list=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body is not None:
        msg.html = html_body
    if attachments is not None:
        for byte in attachments:
            msg.attach("image.png", "image/png", byte)
            
    threading.Thread(target=send_async_email, args=(app, msg)).start()