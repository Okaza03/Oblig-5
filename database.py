from DataBaseConnection import DataBaseConnection
from flask import redirect, url_for
from flask_login import current_user

class DataBase(DataBaseConnection):

    def __init__(self, model):
        self.model = model

    def firstWhere(self, col:str, val: str):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {self.model.table} WHERE {col} = {val}")
            data = db.cursor.fetchone()
        return self.model(*data) if data else None

    def Where(self, col:str, val: str):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {self.model.table} WHERE {col} = {val}")
            data = db.cursor.fetchall()            
        return [self.model(*r) for r in data] if data else None

    def all(self):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {self.model.table}")
            data = db.cursor.fetchall()            
        return [self.model(*r) for r in data] if data else None

    def create_event(self, name, description, date, location):
        with DataBaseConnection as db:
            db.cursor.execute(
                "INSERT INTO event (user_id, name, description, date, location) VALUES (%s, %s, %s, %s, %s)", 
                (current_user, name, description, date, location)
            )
        return redirect(url_for("/my_events"))
