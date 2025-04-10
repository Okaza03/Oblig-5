from flask import url_for
from flask_login import UserMixin


class User(UserMixin):
    table = "user"
    col_count = 6
    fillable=["firstName", "lastName", "email", "password", "image"]
    unique="email"
    
    def __init__(self, id, firstName, lastName, email, password, image=None):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.image = image

    def fullName(self):
        return f"{self.firstName} {self.lastName}"

    def getImage(self):
        return url_for("static", filename=f"uploads/{self.image}") if self.image else url_for('static', filename='default_profile.jpg')
