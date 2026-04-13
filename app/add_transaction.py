import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/finance.db")

def add_transaction(type, category, amount, note=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (type, category, amount, date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (type, category, amount, str(date.today()), note))

    conn.commit()
    conn.close()
    print(f"Added: {type} | {category} | {amount} | {note}")

def main():
    print("=== Cloud Finance Tracker ===")
    type     = input("Type (income/expense): ").strip().lower()
    category = input("Category (food/salary/transport/etc): ").strip().lower()
    amount   = float(input("Amount: ").strip())
    note     = input("Note (optional): ").strip()

    add_transaction(type, category, amount, note)

if __name__ == "__main__":
    main()
