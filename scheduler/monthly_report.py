import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.view_summary import view_summary
from app.alerts import check_alerts
from datetime import datetime

def run_monthly_report():
    print("=" * 50)
    print(f"  Monthly Report — {datetime.today().strftime('%B %Y')}")
    print(f"  Generated at: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    view_summary()
    check_alerts()

    print("\n  Report complete.")
    print("=" * 50)

if __name__ == "__main__":
    run_monthly_report()
