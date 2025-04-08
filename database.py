from DataBaseConnection import DataBaseConnection
from flask import redirect, url_for
from flask_login import current_user


class DataBase(DataBaseConnection):

    def __init__(self, model, load_with=None):
        self.model = model
        self.load_with = load_with

    def _buildQuery(self, query):
        sql = ""
        if self.load_with:
            self.foreign_model, self.foreign_col, self.foreign_key = self.load_with
            sql = f"LEFT JOIN {self.foreign_model.table} as {self.foreign_model.table}_data ON {self.foreign_model.table}_data.{self.foreign_col} = {self.foreign_key}"

        return f"{query} {sql}"


    def _loadWithLogic(self, row):
        model = self.model(*row[: self.model.col_count])
        if self.load_with:
            setattr(
                model,
                self.foreign_model.table,
                self.foreign_model(*row[self.foreign_model.col_count+1:]),
            )

        return model

    def firstWhere(self, col: str, val: str):
        with DataBaseConnection() as db:
            sql = self._buildQuery(f"SELECT * FROM {self.model.table} WHERE {col} = '{val}'")

            db.cursor.execute(sql)
            data = db.cursor.fetchone()

        return self._loadWithLogic(data) if data else None

    def Where(self, col: str, val: str):
        with DataBaseConnection() as db:
            sql = self._buildQuery(f"SELECT * FROM {self.model.table} WHERE {col} = '{val}'")

            db.cursor.execute(sql)
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def all(self):
        with DataBaseConnection() as db:
            sql = self._buildQuery(f"SELECT * FROM {self.model.table}")

            db.cursor.execute(sql)
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def createIfNotExists(self, model):
        if self.model.unique and self.firstWhere(self.model.unique, getattr(self.model.unique, model)):
            return None
        else:
            with DataBaseConnection() as db:
                vals = ",".join(f"'{e}'" for e in [getattr(model, a) for a in self.model.fillable])
                cols = ",".join(self.model.fillable)
                db.cursor.execute(f"INSERT INTO {self.model.table} ({cols}) VALUES ({vals})")
        return True
        
