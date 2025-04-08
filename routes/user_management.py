from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import DataBase
from models.User import User


users_bp = Blueprint('users', __name__) # Creates a Blueprint


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['firstName']
        name = request.form['lastName']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        with DataBase() as db:
            db.create_user(name, email, password)
        return redirect( url_for('users.login') )
    return render_template("user/signup.html")


@users_bp.route('/login', methods=['GET', 'POST'])
def login():        
        if current_user.is_authenticated: return redirect(url_for('index'))
        
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            user = DataBase(User).firstWhere("email", email)
        
            if user and check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for('home') )

            return render_template('session/login.html', error="Invalid credentials")
            
        return render_template("session/login.html")


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for("users.login"))
