import sqlite3
import datetime

table_query='''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
'''


class DiaryRepo:
    def __init__(self):
        with ConnectDB() as (cursor, conn):
            if cursor and conn:
                cursor.execute(table_query)
                conn.commit()


    def create_user(self,full_name,email,password):
        try:
            with ConnectDB() as (cursor, conn):
                query="INSERT INTO users (full_name, email, password)VALUES (?, ?, ?)"
                data=(full_name,email,password)
                cursor.execute(query,data)
                conn.commit()
                return "success"

        except Exception as ex:
            print(f"Exception in create_user as ex =>{ex}")
            return "error"


    def verify_user(self,email,password):
        with ConnectDB() as (cursor, conn):
            cursor.execute("select id from users where email=? and password=?",(email,password))
            res=cursor.fetchone()
            if res:
                return "success",res[0]
            else:
                return "error"

    def get_user_details(self,userid):
        with ConnectDB() as (cursor, conn):
            cursor.execute("select full_name,email from users where id=?", (userid,))
            res = cursor.fetchone()
            if res:
                return "success",res
            else:
                return "error",None

    def delete_account(self,userid):
        with ConnectDB() as (cursor, conn):
            cursor.execute("delete from users where id=?", (userid,))
            affected = cursor.rowcount  # number of rows deleted
            print("Delete account affected =>",affected)
            if affected > 0:
                return "success"
            else:
                return "error"

    def update_user(self, userid, username=None, email=None):
        with ConnectDB() as (cursor, conn):
            cursor.execute(
                "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
                (username, email, userid)
            )
            affected = cursor.rowcount
            conn.commit()
            if affected > 0:
                return "success", affected
            else:
                return "error", 0


    def store_user_analysis(self):
        print("store user prediction and suggestions ")



class ConnectDB:
    def __init__(self):
        self.db_file = "example.db"
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)  # Connect to the SQLite DB
            self.cursor = self.conn.cursor()  # Create a cursor object to interact with the database
            return self.cursor, self.conn
        except sqlite3.Error as ex:
            print("error while connecting as ",ex)
            return None, None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()  # Close the cursor object
        if self.conn:
            self.conn.close()  # Close the database connection
        # Handle exceptions if needed


    def __del__(self):
        print("ConnectDB object destroyed successfully")

