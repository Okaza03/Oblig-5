from config import app, login_manager, render_template, request, mail
from routes import event_bp, user_bp

from database import DataBase
from models.Event import Event
from models.User import User
from mailbox import Message


app.register_blueprint(user_bp)
app.register_blueprint(event_bp)


@login_manager.user_loader
def load_user(user_id):
    return DataBase(User).firstWhere("id", user_id)


# Handlers
@app.errorhandler(404)
def notFound(e):
    return render_template("404.html")


@app.route("/send_mail")
def index():
    mail_message = Message(
        "Hi ! Don’t forget to follow me for more article!",
        sender="your_mail@gmail.com",
        recipients=["to@gmail.com"],
    )
    mail_message.body = "This is a test"
    mail.send(mail_message)
    return "Mail has sent"


# Routes
@app.route("/")
def home():
    query = request.args.get("q")

    if query:
        events = DataBase(Event, load_with=(User, "id", "user_id")).WhereLike(
            "name", query
        )
    else:
        events = DataBase(Event, load_with=(User, "id", "user_id")).all()

    return render_template("index.html", events=events, title="Home")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="localhost")
