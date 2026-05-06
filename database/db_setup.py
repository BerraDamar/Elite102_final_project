import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection to SQLite DB successful: {db_file}")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    """Create a table in the SQLite database."""
    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS users (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT NOT NULL,
                                  age INTEGER,
                                  email TEXT NOT NULL UNIQUE
                              );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def initialize_database(db_file):
    """Initialize the database by creating a connection and setting up tables."""
    conn = create_connection(db_file)
    if conn:
        create_table(conn)
