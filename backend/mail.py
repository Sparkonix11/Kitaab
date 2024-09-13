from factory import mail
from flask_mail import Message
def send_email(email, subject, message):
            msg = Message(recipients=[email],
                          body = message,
                          subject=subject
                          )
            mail.send(msg)