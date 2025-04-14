from flask import Flask
from flask_mail import Mail
from routes import event_bp, user_bp
from flask_mail import Mail, Message
from flask_login import LoginManager, login_required, current_user
from flask import render_template, request
from flask_wtf.csrf import CSRFProtect

import os


app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "your_mail@gmail.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = Truemail = Mail(app)


app.secret_key = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static", "uploads"
)

app.register_blueprint(user_bp)
app.register_blueprint(event_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

csrf = CSRFProtect()
csrf.init_app(app)
