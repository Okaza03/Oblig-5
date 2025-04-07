import mysql.connector
from DataBaseConnection import DataBaseConnection

class DataBase(DataBaseConnection):

    @classmethod
    def firstWhere(cls, model, col:str, val: str):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {model.table} WHERE {col} = {val}")
            data = db.cursor.fetchone()
        return model(*data) if data else None

    @classmethod
    def Where(cls, model, col:str, val: str):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {model.table} WHERE {col} = {val}")
            data = db.cursor.fetchall()            
        return model(*data) if data else None

    @classmethod
    def all(cls, model):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {model.table}")
            data = db.cursor.fetchall()            
        return model(*data) if data else None

    
