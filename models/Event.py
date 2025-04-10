

from flask import url_for
from models.User import User


class Event():
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

    def getImage(self):
        return url_for("static", filename=f"uploads/{self.image}") if self.image else f"https://picsum.photos/300/100?random={self.id}"
        
