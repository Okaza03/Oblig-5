from DataBaseConnection import DataBaseConnection
from flask import redirect, url_for
from flask_login import current_user

class DataBase(DataBaseConnection):

    def __init__(self, model, load_with=None):
        self.model = model
        self.load_with = load_with

        self.add_to_query = None
        if self.load_with:
            self.foreign_model, self.foreign_col, self.foreign_key = self.load_with
            sql = f"LEFT JOIN {self.foreign_model.table} as {self.foreign_model.table}_data ON {self.foreign_model.table}_data.{self.foreign_col} = {self.foreign_key}"
            self.add_to_query = sql
        

    def _loadWithLogic(self, row):
            if self.load_with:
                row = row[1:]
        
            model = self.model(*row[:self.model.col_count])
            if self.foreign_model:
                setattr(model, self.foreign_model.table, self.foreign_model(*row[self.foreign_model.col_count:]))

            return model

    def firstWhere(self, col:str, val: str):
        with DataBaseConnection() as db:
            sql = f"SELECT * FROM {self.model.table} WHERE {col} = {val}"
            if self.load_with: sql = f"{sql} {self.add_to_query}"
            
            db.cursor.execute(sql)
            data = db.cursor.fetchone()
            
        return self._loadWithLogic(data) if data else None

    def Where(self, col:str, val: str):
        with DataBaseConnection() as db:
            sql = f"SELECT * FROM {self.model.table} WHERE {col} = {val}"
            if self.load_with: sql = f"{sql} {self.add_to_query}"
            
            db.cursor.execute(sql)
            data = db.cursor.fetchall()            

        return [self._loadWithLogic(r) for r in data] if data else None

    def all(self):
        with DataBaseConnection() as db:
            sql = f"SELECT * FROM {self.model.table}"
            if self.load_with: sql = f"{sql} {self.add_to_query}"
            
            db.cursor.execute(sql)
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def create_event(self, name, description, date, location):
        with DataBaseConnection as db:
            db.cursor.execute(
                "INSERT INTO event (user_id, name, description, date, location) VALUES (%s, %s, %s, %s, %s)", 
                (current_user, name, description, date, location)
            )
        return redirect(url_for("/my_events"))
