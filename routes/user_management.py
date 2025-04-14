from config import (
    render_template,
    redirect,
    url_for,
    login_required,
    login_user,
    logout_user,
    generate_password_hash,
    check_password_hash,
    secure_filename,
    allowed_file,
    flash,
    request,
    current_app,
    current_user,
    mail,
    Blueprint,
    os,
)

from database import DataBase
from models.User import User
from utils.mail import send_verification_email, send_password_reset_email
from utils.token import (
    confirm_password_token,
    confirm_email_token,
)

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
                current_user.id,
                firstName,
                lastName,
                email,
                current_user.password,
                custom_filename,
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
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = DataBase(User).firstWhere("email", email)

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for("home"))

        return render_template("user/login.html", error="Invalid credentials")

    return render_template("user/login.html", title="Login")


@user_bp.route("/verify-email-request", methods=["GET"])
@login_required
def verify_email_request():
    if current_user.email_verified:
        flash("Your email is already verified.", "info")
    else:
        send_verification_email(current_user)
        flash("Verification email sent! Please check your inbox.", "email")

    return redirect(url_for("user.profile"))


@user_bp.route("/verify-email/<token>")
def verify_email(token):
    email = confirm_email_token(token)
    if not email:
        flash("Verification link is invalid or has expired.", "error")
        return redirect(url_for("user.profile"))

    user = DataBase(User).firstWhere("email", email)
    if user:
        user.email_verified = 1
        DataBase(User).update(user)
        flash("Your email has been verified!", "email")
        return redirect(url_for("user.profile"))

    flash("User not found.", "error")
    return redirect(url_for("user.profile"))


@user_bp.route("/send-password-reset", methods=["GET"])
@login_required
def send_password_reset():
    send_password_reset_email(current_user)
    flash("Password change email sent! Please check your inbox.", "password")

    return redirect(url_for("user.profile"))


@user_bp.route("/profile/change-password/<token>", methods=["GET", "POST"])
def change_password(token):
    email = confirm_password_token(token)
    if not email:
        flash("Invalid or expired token.", "error")
        return redirect(url_for("user.login"))

    user = DataBase(User).firstWhere("email", email)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("user.login"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        user.password = generate_password_hash(new_password)
        DataBase(User).update(user)
        flash("Your password has been changed successfully.", "password")
        return redirect(url_for("user.profile"))

    return render_template("user/change-password.html", token=token)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
