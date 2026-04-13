import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/finance.db")

def view_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current month in YYYY-MM format
    month = datetime.today().strftime("%Y-%m")

    print(f"\n=== Finance Summary for {month} ===\n")

    # Total income
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'income' AND date LIKE ?
    """, (f"{month}%",))
    total_income = cursor.fetchone()[0]

    # Total expenses
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'expense' AND date LIKE ?
    """, (f"{month}%",))
    total_expenses = cursor.fetchone()[0]

    balance = total_income - total_expenses

    print(f"  Total Income   : {total_income:>10.2f}")
    print(f"  Total Expenses : {total_expenses:>10.2f}")
    print(f"  Balance        : {balance:>10.2f}")

    print(f"\n--- Expense Breakdown by Category ---\n")

    # Category wise breakdown
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense' AND date LIKE ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (f"{month}%",))
    rows = cursor.fetchall()

    if rows:
        for category, amount in rows:
            print(f"  {category:<15} : {amount:>10.2f}")
    else:
        print("  No expenses recorded this month.")

    print(f"\n--- All Transactions This Month ---\n")

    cursor.execute("""
        SELECT date, type, category, amount, note
        FROM transactions
        WHERE date LIKE ?
        ORDER BY date ASC
    """, (f"{month}%",))
    all_rows = cursor.fetchall()

    if all_rows:
        print(f"  {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10}  Note")
        print("  " + "-" * 60)
        for date, type, category, amount, note in all_rows:
            print(f"  {date:<12} {type:<10} {category:<15} {amount:>10.2f}  {note or ''}")
    else:
        print("  No transactions found.")

    conn.close()

if __name__ == "__main__":
    view_summary()
