from flask import Flask, flash
from flask_mail import Mail, Message
from flask_login import (
    LoginManager,
    login_required,
    logout_user,
    login_user,
    current_user,
)
from flask import render_template, redirect, url_for, request, Blueprint, current_app
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from files import allowed_file


app = Flask(__name__)
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True


app.secret_key = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static", "uploads"
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

mail = Mail(app)

csrf = CSRFProtect()
csrf.init_app(app)
