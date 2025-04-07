import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class DataBaseConnection():

    def __init__(self):
        self.mysqlConnector = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
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
