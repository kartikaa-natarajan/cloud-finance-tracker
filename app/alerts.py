import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/finance.db")

# Set your budget limits per category (monthly)
BUDGET_LIMITS = {
    "food"         : 3000,
    "transport"    : 2000,
    "utilities"    : 3000,
    "entertainment": 2000,
    "health"       : 3000,
    "other"        : 2000,
}

def check_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    month = datetime.today().strftime("%Y-%m")

    print(f"\n=== Budget Alert Check for {month} ===\n")

    alert_found = False

    for category, limit in BUDGET_LIMITS.items():
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM transactions
            WHERE type = 'expense'
            AND category = ?
            AND date LIKE ?
        """, (category, f"{month}%"))

        spent = cursor.fetchone()[0]

        if spent > limit:
            print(f"  ⚠️  WARNING: {category} spending ({spent:.2f}) exceeded budget limit ({limit})!")
            alert_found = True
        elif spent > limit * 0.8:
            print(f"  🔔  NOTICE: {category} spending ({spent:.2f}) is close to budget limit ({limit})!")
            alert_found = True
        else:
            print(f"  ✅  {category:<15} : spent {spent:>8.2f} / limit {limit:>8.2f}")

    if not alert_found:
        print("\n  All spending within budget. Great job!")

    conn.close()

if __name__ == "__main__":
    check_alerts()
