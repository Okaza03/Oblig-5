from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from database import DataBase
from models.Event import Event
from routes import event_bp, user_bp
from models.User import User
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)
app.config["UPLOAD_FOLDER"] = os.path.join(BASEDIR, "static", "uploads")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.login"


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
        events = DataBase(Event, load_with=(User, "id", "user_id")).WhereLike(
            "name", query
        )
    else:
        events = DataBase(Event, load_with=(User, "id", "user_id")).all()

    return render_template(
        "index.html",
        events=events,
        title="Home",
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        date = request.form.get("date")
        location = request.form.get("location")
        image = request.files.get("image")

        new_event = Event(
            None, current_user.id, name, description, date, location
        )  # Todo: id nullable

        if not DataBase(Event).createIfNotExists(new_event):
            return render_template(
                "event/create-event.html", error="Something went wrong"
            )

        if image:
            file = image

            if not file.filename == "":
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    name_part, ext = os.path.splitext(filename)
                    custom_filename = f"{current_user.id}{ext}"

                    print(custom_filename)
                    file.save(
                        os.path.join(app.config["UPLOAD_FOLDER"], custom_filename)
                    )

        return redirect(url_for("my_events"))

    return render_template("event/create-event.html", title="Create Event")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="localhost")
