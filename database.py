import mysql.connector
from DataBaseConnection import DataBaseConnection

class DataBase(DataBaseConnection):

    # Methods
    @classmethod
    def firstWhere(cls, model, col:str, val: str):
        with DataBaseConnection() as db:
            db.cursor.execute(f"SELECT * FROM {model.table} WHERE {col} = {val}")
            data = db.cursor.fetchone()
            
        return model(*data) if data else None
