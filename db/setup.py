import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "finance.db")

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            type     TEXT NOT NULL,
            category TEXT NOT NULL,
            amount   REAL NOT NULL,
            date     TEXT NOT NULL,
            note     TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()
