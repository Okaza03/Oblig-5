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

# Routes
@app.route("/")
def home():
    #return DataBase.firstWhere(User, "id", "1")
    return render_template("index.html", user=current_user)

# Handlers
@app.errorhandler(404)
def notFound(e): return render_template("404.html")




if __name__ == "__main__":
    app.run(debug=True)
