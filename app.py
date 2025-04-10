from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from database import DataBase
from models.Event import Event
from routes.user_management import user_bp
from models.User import User
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/static/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.register_blueprint(user_bp)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
    return render_template(
        "index.html", events=DataBase(Event, load_with=(User, "id", "user_id")).all()
    )


@app.route("/my-events")
@login_required
def my_events():
    return render_template(
        "event/my-events.html",
        my_events=DataBase(Event).Where("user_id", current_user.id),
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

        new_event = Event(
            None, "2", name, description, date, location
        )  # Todo: id nullable

        if not DataBase(Event).createIfNotExists(new_event):
            return render_template(
                "event/create-event.html", error="Something went wrong"
            )


        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))


        return redirect(url_for("my_events"))

    return render_template("event/create-event.html")


if __name__ == "__main__":
    app.run(debug=True)
