from config import mail, url_for, Message
from utils.token import generate_email_token, generate_password_token


def send_verification_email(user):
    token = generate_email_token(user.email)
    verify_link = url_for("user.verify_email", token=token, _external=True)

    msg = Message(
        subject="Verify your email address",
        sender="management.eventhub@gmail.com",
        recipients=[user.email],
    )
    msg.body = (
        f"Hello {user.firstName},\n\nPlease verify your email address:\n{verify_link}"
    )
    mail.send(msg)


def send_password_reset_email(user):
    token = generate_password_token(user.email)
    reset_link = url_for("user.change_password", token=token, _external=True)

    msg = Message(
        "Change your password",
        sender="management.eventhub@gmail.com",
        recipients=[user.email],
    )
    msg.body = f"Hi {user.firstName},\n\nClick the link below to change your password:\n\n{reset_link}"
    mail.send(msg)
