from flask import url_for
from database import DataBase


class Event:
    table = "event"
    col_count = 7
    fillable = ["user_id", "name", "description", "date", "location", "image"]
    unique = None

    def __init__(self, id, user_id, name, description, date, location, image=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.date = date
        self.location = location
        self.image = image

    def manager(self):
        from models.User import User

        return DataBase(User).firstWhere("id", self.user_id)

    def users(self):
        from models.User import User

        return DataBase(User).hasMany(self, "event_has_user", "event_id", "user_id")

    def getImage(self):
        return (
            url_for("static", filename=f"uploads/{self.image}")
            if self.image
            else url_for("static", filename=f"default-image.png")
        )
