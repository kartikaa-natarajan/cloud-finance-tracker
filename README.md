# Cloud Finance Tracker

A personal finance tracking system deployed on a Linux cloud VM (AWS EC2). Built with Python and SQLite to log transactions, generate monthly summaries and trigger budget alerts via automated cron jobs.

## Tech Stack
- Python 3.12
- SQLite3
- Linux (Ubuntu 24.04)
- AWS EC2 (t3.micro)
- Git & GitHub
- Cron Jobs

## Features
- Log income and expenses with category and notes
- View monthly summary with total income, expenses and balance
- Category wise expense breakdown
- Budget alerts when spending exceeds set limits
- Automated monthly report via cron job on cloud VM

## How to Run

1. Set up the database: python3 db/setup.py
2. Add a transaction: python3 app/add_transaction.py
3. View monthly summary: python3 app/view_summary.py
4. Check budget alerts: python3 app/alerts.py
5. Run full report: python3 scheduler/monthly_report.py

## Database Schema
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto incrementing ID |
| type | TEXT | income or expense |
| category | TEXT | food, salary, transport |
| amount | REAL | Transaction amount |
| date | TEXT | Date in YYYY-MM-DD |
| note | TEXT | Optional note |

## Author
Built as a portfolio project to demonstrate Python, SQL, Linux and cloud infrastructure skills.
