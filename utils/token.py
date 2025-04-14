from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_email_token(email):
    s = URLSafeTimedSerializer(current_app.secret_key)
    return s.dumps(email, salt="email-confirm")


def confirm_email_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.secret_key)
    try:
        email = s.loads(token, salt="email-confirm", max_age=expiration)
    except Exception:
        return None
    return email


def generate_password_token(email):
    s = URLSafeTimedSerializer(current_app.secret_key)
    return s.dumps(email, salt="password-reset")


def confirm_password_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.secret_key)
    try:
        email = s.loads(token, salt="password-reset", max_age=expiration)
    except:
        return None
    return email
