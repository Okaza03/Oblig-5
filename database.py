import mysql.connector
from DataBaseConnection import DataBaseConnection

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

    
