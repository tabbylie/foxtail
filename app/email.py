from flask_mail import Message
from app import app, mail
import threading

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[FOXTAIL] Password Reset',
        sender=app.config['ADMINS'][0], recipients=[user.email],
         text_body=render_template(app.config['EMAIL_TEXT_TEMPLATE_FOLDER'] + 'password_reset.txt', user=user, token=token),
         html_body=render_template(app.config['EMAIL_HTML_TEMPLATE_FOLDER'] + 'password_reset.html', user=user, token=token)
    )
    
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