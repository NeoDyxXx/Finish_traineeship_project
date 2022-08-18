import random

from flask_mail import Message

from user_auth.flask_app import mail, app


def generate_otp(otp_size=6) -> str:
    final_code = ''
    for i in range(otp_size):
        final_code += str(random.randint(0, 9))
    return final_code


def send_email(email: str, otp_code: str):
    msg = Message(subject='Visa Helper Verification', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = ' '.join(['Your verification OTP code:', otp_code])
    mail.send(msg)
