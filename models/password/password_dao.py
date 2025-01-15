import sqlite3
from models.password_value.password_value import PasswordValue
from utils.logger import log
import traceback


def connection(*args):
    con = sqlite3.connect('models/automation.db')
    con.execute('PRAGMA foreign_keys = ON;')
    return con


class PasswordDAO:
    """
    Passwords class to manage data (puto el que lee jaja xd lol)
    """
    def create_table():
        con = connection('automation.db')
        cursor = con.cursor()
        
        query = """
                CREATE TABLE IF NOT EXISTS passwords(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value BLOB NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                )
                """
        
        try:
            cursor.execute(query)
            con.commit()
        except ConnectionError as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()

    def create(password: PasswordValue, user_id: int):
        con = connection()
        cursor = con.cursor()

        query = """
                INSERT INTO passwords(value, user_id) VALUES(?, ?)
                """
        
        try:
            cursor.execute(query, (password.crypted_password, user_id))
            con.commit()
        except ConnectionError as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()

    def get_all(user_id) -> list:
        con = connection()
        cursor = con.cursor()

        query = """
                SELECT * FROM passwords WHERE user_id = ? ORDER BY id ASC
                """
        try:
            data = cursor.execute(query, (user_id,))
            con.commit()
            passwords = data.fetchall()
            
            return passwords
        except ConnectionError as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()

    def delete(password_id, user_id):
        con = connection()
        cursor = con.cursor()

        query = """
                DELETE FROM passwords WHERE id = ? and user_id = ?
                """
        
        try:
            cursor.execute(query, (password_id, user_id))
            con.commit()
        except ConnectionError as e:
            log(f'{__file__} - {traceback.format_exc()}')
        finally:
            con.close()