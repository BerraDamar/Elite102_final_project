import sqlite3

DB_NAME = "example.db"

def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== INITIALIZING DATABASE ===")

    # Create accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            balance REAL
        )
    ''')

    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            type TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert sample accounts ONLY if table is empty
    cursor.execute("SELECT COUNT(*) FROM account")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Inserting sample accounts...")
        cursor.execute('''
            INSERT INTO account (name, balance) VALUES
            ('Anna', 1000),
            ('Berra', 2000),
            ('Zumra', 1000),
            ('Ameena', 1200)
        ''')
    else:
        print("Sample accounts already exist. Skipping insert.")

    connection.commit()
    connection.close()
    print("Database initialization complete.")


initialize_database()
