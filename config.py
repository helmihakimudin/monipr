import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # ganti sesuai user MySQL
        password="",       # ganti sesuai password MySQL
        database="monipr"
    )
