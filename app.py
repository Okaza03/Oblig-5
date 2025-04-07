from flask import Flask, render_template
from flask_login import LoginManager, login_required, login_remembered, current_user
from database import DataBase
from models.user import User
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    with DataBase() as db:
        user = db.load_user(user_id)
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None


@app.route("/")
def home():

    return render_template("index.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
