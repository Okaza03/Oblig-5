from DataBaseConnection import DataBaseConnection

class DataBase(DataBaseConnection):

    def __init__(self, model, load_with=None):
        self.model = model
        self.load_with = load_with

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
            sql = f"SELECT * FROM {self.model.table}"

            if self.load_with:
                foreign_model, foreign_col, foreign_key = self.load_with
                sql = f"{sql} LEFT JOIN {foreign_model.table} as {foreign_model.table}_data ON {foreign_model.table}_data.{foreign_col} = {foreign_key}"
            
            db.cursor.execute(sql)
            data = db.cursor.fetchall()

        result = []
        for row in data:
            if self.load_with:
                row = row[1:]
        
            model = self.model(*row[:self.model.col_count])
            if foreign_model:
                setattr(model, foreign_model.table, foreign_model(*row[foreign_model.col_count:]))
            result.append(model)
            
        return result

    
    def create_event(self):
        return