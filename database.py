import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()


class DataBase:
    def __init__(self):
        self.mysqlConnector = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            name=os.getenv("DB_NAME"),
        )

    def __enter__(self):
        try:
            self.cursor = self.mysqlConnector.cursor()
            return self
        except mysql.connector.Error as error:
            print("Error while connecting to MySQL", error)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysqlConnector.commit()
        self.cursor.close()
        self.mysqlConnector.close()

    def load_user(self, user_id):
        self.cursor.execute("SELECT * FROM user WHERE id = %s", (user_id))
        return self.cursor.fetchone()

    def create_user(self, FirstName, LastName, Email, Password):
        self.cursor.execute(
            "INSERT INTO user (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s)",
            (FirstName, LastName, Email, Password),
        )
        return

    def load_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM user WHERE email = %s", (email))
        return self.cursor.fetchone()
