from DataBaseConnection import DataBaseConnection


class DataBase(DataBaseConnection):

    def __init__(self, model, load_with=None):
        self.model = model
        self.load_with = load_with
        if load_with:
            self.foreign_model, self.foreign_col, self.foreign_key = load_with

    def _buildQuery(self, select_query, where_query=""):
        sql_a = ""
        if self.load_with:
            self.foreign_model, self.foreign_col, self.foreign_key = self.load_with
            sql_a = f"LEFT JOIN {self.foreign_model.table} as {self.foreign_model.table}_data ON {self.foreign_model.table}_data.{self.foreign_col} = {self.foreign_key}"

        return f"{select_query} {sql_a} {where_query}"

    def _loadWithLogic(self, row):
        model = self.model(*row[: self.model.col_count])
        if self.load_with:
            setattr(
                model,
                self.foreign_model.table,
                self.foreign_model(*row[self.foreign_model.col_count + 1 :]),
            )

        return model

    def firstWhere(self, col: str, val: str, additional=None):
        with DataBaseConnection() as db:
            
            sql = self._buildQuery(
                f"SELECT * FROM {self.model.table}",
                f"WHERE {col} = %s",
            )

            if additional:
                ad_q, ad_val = additional
                sql += f"{ad_q}"
                db.cursor.execute(sql, (val,ad_val))
            else:
                db.cursor.execute(sql, (val,))
                
                
            data = db.cursor.fetchone()

        return self._loadWithLogic(data) if data else None

    def Where(self, col: str, val: str):
        with DataBaseConnection() as db:
            sql = self._buildQuery(
                f"SELECT * FROM {self.model.table}", f"WHERE {col} = %s"
            )

            db.cursor.execute(sql, (val, ))
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def WhereLike(self, col: str, val: str):
        with DataBaseConnection() as db:
            sql = self._buildQuery(
                f"SELECT * FROM {self.model.table}", f"WHERE {col} like %s"
            )

            db.cursor.execute(sql, (f"%{val}%",))
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def all(self):
        with DataBaseConnection() as db:
            sql = self._buildQuery(f"SELECT * FROM {self.model.table}")

            db.cursor.execute(sql)
            data = db.cursor.fetchall()

        return [self._loadWithLogic(r) for r in data] if data else None

    def createIfNotExists(self, model):
        existing = None
        if self.model.unique:
            existing = self.firstWhere(self.model.unique, getattr(model, self.model.unique))

        if existing:
            # Returner eksisterende modell med riktig ID
            return existing
        else:
            with DataBaseConnection() as db:
                vals = [getattr(model, a) for a in self.model.fillable]
                cols = ",".join(self.model.fillable)
                placeholders = ",".join(["%s"] * len(vals))
                db.cursor.execute(
                    f"INSERT INTO {self.model.table} ({cols}) VALUES ({placeholders})", vals
                )
                setattr(model, "id", db.cursor.lastrowid)
            return model


    def update(self, model):
        if self.model.unique and self.firstWhere(
            self.model.unique,
            getattr(model, self.model.unique),
            additional=(f"AND id != %s", model.id),
        ):
            return None
        else:
            with DataBaseConnection() as db:
                vals = [getattr(model, a) for a in self.model.fillable]
                cols = self.model.fillable
                update = ", ".join(f"{col} = %s" for col in cols)
                sql = f"UPDATE {self.model.table} SET {update} WHERE id = %s"
                db.cursor.execute(sql, vals + [model.id])
        return True


    def hasMany(self, model, mtm, m_col, f_col):
        with DataBaseConnection() as db:
            sql = f"""SELECT {self.model.table}.* 
                  FROM {self.model.table} 
                  WHERE {self.model.table}.id IN (
                      SELECT {f_col} 
                      FROM {mtm} 
                      WHERE {m_col} = %s
                  )"""
            db.cursor.execute(sql, (model.id,))
            data = db.cursor.fetchall()
        return [self._loadWithLogic(r) for r in data] if data else None


    def insert_relation(self, model, mtm, m_col, f_col):
        with DataBaseConnection() as db:
            db.cursor.execute(
                f"INSERT INTO {mtm} ({m_col}, {f_col}) VALUES (%s, %s)",
                (self.model.id, model.id),
            )

    def delete_relation(self, model, mtm, m_col, f_col):
        with DataBaseConnection() as db:
            db.cursor.execute(
                f"DELETE FROM {mtm} WHERE {m_col} = %s AND {f_col} = %s",
                (self.model.id, model.id),
            )
