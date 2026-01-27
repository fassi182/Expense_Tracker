import os
from services.expense_service import add_expense, view_report
from services.currency_service import view_all_rates
from services.file_service import write_json
from logger_config import logger  # Import the logger

# ---------------------- Initialization ----------------------
def init_files():
    os.makedirs("data", exist_ok=True)
    logger.info("Ensured 'data' directory exists")

    if not os.path.exists("data/expenses.json"):
        write_json("data/expenses.json", {"expenses": [], "total": 0})
        logger.info("Created 'expenses.json' with default structure")

    if not os.path.exists("data/rates_cache.json"):
        write_json("data/rates_cache.json", {
            "usd": 278.50,
            "eur": 302.10,
            "gbp": 353.40,
            "inr": 3.35,
            "pkr": 1.0
        })
        logger.info("Created 'rates_cache.json' with default rates")

logger.info("Starting Expense Tracker Pro")
init_files()

# ---------------------- Main Menu Loop ----------------------
while True:
    print("\n=========================")
    print("   EXPENSE TRACKER ")
    print("=========================")
    print("1. Add Expense")
    print("2. View Report")
    print("3. View Exchange Rates")
    print("4. Exit")

    choice = input("\nEnter Choice: ").strip()
    logger.info(f"User selected menu option: {choice}")

    if choice == "1":
        logger.info("User chose to add a new expense")
        add_expense()
    elif choice == "2":
        logger.info("User chose to view expense report")
        view_report()
    elif choice == "3":
        logger.info("User chose to view exchange rates")
        view_all_rates()
    elif choice == "4":
        logger.info("User exited the application")
        print("Exiting Expense Tracker Pro. Goodbye!")
        break
    else:
        logger.warning(f"User entered invalid menu option: {choice}")
        print("❌ Invalid option. Please select 1-4.")
