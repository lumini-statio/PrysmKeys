import sqlite3
from models.password_value.password_value import PasswordValue
from utils.logger import log
import traceback


def connection(*args):
    con = sqlite3.connect('models/automation.db')
    con.execute('PRAGMA foreign_keys = ON;')
    return con

class ValueDAO:
    """
    class that manage all passwords values data
    """

    def create_table():
        con = connection()
        cursor = con.cursor()

        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS password_values(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crypted_password BLOB NOT NULL,
                key TEXT NOT NULL,
                password_id INTEGER,
                FOREIGN KEY (password_id) REFERENCES passwords (id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
                )
                """
            )
            con.commit()
        except ConnectionError as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()
    
    @staticmethod
    def create(password_value: PasswordValue):
        con = connection()
        cursor = con.cursor()

        query = "INSERT INTO password_values(crypted_password, key, password_id) VALUES(?, ?, ?)"

        try:
            cursor.execute(query, (password_value.crypted_password, password_value.get_key_str(), password_value.password_id))
            con.commit()
            con.close()
            return password_value
        except ConnectionError as e:
            log(f'{__file__} - {e}\nproblem with value creating function')
        finally:
            con.close()

    def get_all():
        con = connection()
        cursor = con.cursor()

        try:
            values = cursor.execute("SELECT * FROM password_values ORDER BY id ASC")
            con.commit()
            data = values.fetchall()
            con.close()
            return data
        except ConnectionError as e:
            log(f'{__file__} - {e}\nproblem with value selection function')
        
        con.close()

    def delete(password_id):
        con = connection()
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM password_values WHERE password_id = ?", (password_id,))
            con.commit()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()