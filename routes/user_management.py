from flask import render_template, redirect, url_for, request, Blueprint, current_app
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import DataBase
from models.User import User
import os
from werkzeug.utils import secure_filename
from files import allowed_file

app = current_app

user_bp = Blueprint("user", __name__)  # Creates a Blueprint


@user_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = request.form["password"]
        image = request.files.get("image")
        
        errors = []
        custom_filename = current_user.image
        
        if image:
            file = image
            if not file.filename == "":
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    name_part, ext = os.path.splitext(filename)
                    custom_filename = f"user_{current_user.id}{ext}"

                    file.save(
                        os.path.join(app.config["UPLOAD_FOLDER"], custom_filename)
                    )


        if check_password_hash(current_user.password, password):
            updated_user = User(
                current_user.id, firstName, lastName, email, current_user.password, custom_filename
            )

            if not DataBase(User).update(updated_user):
                errors.append("Email already in use")
            else:
                login_user(updated_user)
        else:
            errors.append("Incorrect password")

        return render_template("user/profile.html", user=current_user, errors=errors)

    return render_template("user/profile.html", user=current_user, title="Profile")


@user_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        new_user = User(None, firstName, lastName, email, password)
        if not DataBase(User).createIfNotExists(new_user):
            return render_template("user/signup.html", error="Email already in use")

        return redirect(url_for("user.login"))
    return render_template("user/signup.html", title="Signup")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = DataBase(User).firstWhere("email", email)

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for("home"))

        return render_template("user/login.html", error="Invalid credentials")

    return render_template("user/login.html", title="Login")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
