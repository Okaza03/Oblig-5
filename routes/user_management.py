from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import DataBase
from models.User import User


users_bp = Blueprint('users', __name__) # Creates a Blueprint


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        new_user = User(None, firstName, lastName, email, password)
        if not DataBase(User).createIfNotExists(new_user):
            return render_template('users/signup.html', error="Email already in use")

        return redirect(url_for('users.login') )
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

            return render_template('users/login.html', error="Invalid credentials")
            
        return render_template("users/login.html")


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
        
