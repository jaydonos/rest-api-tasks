import sqlite3

DATABASE_NAME = "tasks.db"

#Open database
def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row #Access columns by name
    return conn

#Read schema and create tables
def init_db():
    with get_connection() as conn:
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read()) #Used for multiple sql statements
