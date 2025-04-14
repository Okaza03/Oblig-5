from flask import url_for
from flask_login import UserMixin

from database import DataBase

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

    def attends(self, event):
        from models.Event import Event
        return DataBase(self).insert_relation(event, "event_has_user", "user_id", "event_id")

    def notAttends(self, event):
        from models.Event import Event        
        return DataBase(self).delete_relation(event, "event_has_user", "user_id", "event_id")

    def events(self):
        from models.Event import Event
        return DataBase(Event).hasMany(self, "event_has_user", "user_id", "event_id")

    def getImage(self):
        return url_for("static", filename=f"uploads/{self.image}") if self.image else url_for('static', filename='default_profile.jpg')
