import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/finance.db")

# Your email settings
SENDER_EMAIL   = "karnatarajan23@gmail.com"
APP_PASSWORD   = "vturmmquljxetvax"
RECEIVER_EMAIL = "karnatarajan23@gmail.com"

BUDGET_LIMITS = {
    "food"         : 3000,
    "transport"    : 2000,
    "utilities"    : 3000,
    "entertainment": 2000,
    "health"       : 3000,
    "other"        : 2000,
}

def build_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    month = datetime.today().strftime("%Y-%m")

    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='income' AND date LIKE ?", (f"{month}%",))
    total_income = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='expense' AND date LIKE ?", (f"{month}%",))
    total_expenses = cursor.fetchone()[0]

    balance = total_income - total_expenses

    cursor.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE type='expense' AND date LIKE ?
        GROUP BY category ORDER BY SUM(amount) DESC
    """, (f"{month}%",))
    categories = cursor.fetchall()

    lines = []
    lines.append(f"Finance Report — {datetime.today().strftime('%B %Y')}")
    lines.append("=" * 40)
    lines.append(f"Total Income   : {total_income:>10.2f}")
    lines.append(f"Total Expenses : {total_expenses:>10.2f}")
    lines.append(f"Balance        : {balance:>10.2f}")
    lines.append("")
    lines.append("Expense Breakdown:")
    for cat, amt in categories:
        lines.append(f"  {cat:<15} : {amt:>8.2f}")

    lines.append("")
    lines.append("Budget Alerts:")
    for category, limit in BUDGET_LIMITS.items():
        cursor.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='expense' AND category=? AND date LIKE ?", (category, f"{month}%"))
        spent = cursor.fetchone()[0]
        if spent > limit:
            lines.append(f"  WARNING : {category} ({spent:.2f}) exceeded limit ({limit})")
        elif spent > limit * 0.8:
            lines.append(f"  NOTICE  : {category} ({spent:.2f}) close to limit ({limit})")
        else:
            lines.append(f"  OK      : {category} ({spent:.2f}) / {limit}")

    conn.close()
    return "\n".join(lines)

def send_email():
    report = build_report()
    month  = datetime.today().strftime("%B %Y")

    msg = MIMEMultipart()
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECEIVER_EMAIL
    msg["Subject"] = f"Finance Report — {month}"
    msg.attach(MIMEText(report, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

    print("Email sent successfully!")

if __name__ == "__main__":
    send_email()
