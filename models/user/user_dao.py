import sqlite3
import traceback


def connection(*args):
    con = sqlite3.connect('data.db')
    con.execute('PRAGMA foreign_keys = ON;')
    return con


class UserDAO():
    """
    Users database actions
    """
    def create_table():
        con = connection()
        cursor = con.cursor()
        
        query = """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(20) NOT NULL,
                    password TEXT NOT NULL
                )
                """
        
        try:
            cursor.execute(query)
            con.commit()
        except ConnectionError as e:
            pass
        finally:
            con.close()

    def create(username, password):
        con = connection()
        cursor = con.cursor()

        query = """
                INSERT INTO users(username, password) VALUES(?, ?)
                """

        try:
            cursor.execute(query, (username, password))
            con.commit()
        except ConnectionError as e:
            pass
        finally:
            con.close()

    def get_all():
        con = connection()
        cursor = con.cursor()

        query = """
                SELECT * FROM users ORDER BY id ASC
                """
        
        try:
            data = cursor.execute(query)
            con.commit()
            users = data.fetchall()

            return users
        except ConnectionError as e:
            pass
        finally:
            con.close()

    def delete(user_id):
        con = connection()
        cursor = con.cursor()

        query = """
                DELETE FROM users WHERE id = ?
                """
        
        try:
            cursor.execute(query, (user_id,))
            con.commit()
        except ConnectionError as e:
            pass
        finally:
            con.close()