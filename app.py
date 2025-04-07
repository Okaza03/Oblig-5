from flask import Flask, render_template
from flask_login import LoginManager, login_required, login_remembered, current_user
from database import DataBase
from routes.user_management import users_bp
from models.user import User
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(users_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return DataBase.firstWhere(User, "id", user_id)

# Handlers
@app.errorhandler(404)
def notFound(e): return render_template("404.html")

# Routes
@app.route("/")
def home():
    return render_template("index.html", user=current_user)

@login_required
@app.route("/my-events")
def event():
    return render_template("/event/my-events.html", )

@login_required
@app.route("/create-event")
def event():
    return render_template("/event/create-event.html", )


if __name__ == "__main__":
    app.run(debug=True)
