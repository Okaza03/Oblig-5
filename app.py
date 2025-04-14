from flask import Flask, render_template, request, redirect, url_for, flash, Response, abort
from flask_login import LoginManager, login_required, current_user, UserMixin, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from database import DataBase
from models.Event import Event
from models.User import User
from routes import event_bp, user_bp
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")

app.register_blueprint(user_bp)
app.register_blueprint(event_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"

csrf = CSRFProtect()
csrf.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return DataBase(User).firstWhere("id", user_id)

# Handlers
@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")

# Routes
@app.route("/")
def home():
    query = request.args.get("q")

    if query:
        events = DataBase(Event, load_with=(User, "id", "user_id")).WhereLike("name", query)
    else:
        events = DataBase(Event, load_with=(User, "id", "user_id")).all()

    return render_template("index.html", events=events, title="Home")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="localhost")
