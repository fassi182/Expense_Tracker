from services.file_service import read_json, write_json
from services.currency_service import get_pkr_rate
from logger_config import logger

JSON_FILE = "data/expenses.json"

CATEGORIES = ["Food", "Travel", "Bills", "Others"]
CURRENCIES = ["USD","EUR","GBP","JPY","AUD","CAD","CHF","CNY","INR","SAR"]

DEFAULT_DATA = {"expenses": [], "total": 0}

# ---------------------- Add Expense ----------------------
def add_expense():
    logger.info("User selected: Add Expense")
    print("\n--- Add New Expense ---")
    
    # Show categories
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    
    cat = input("Select Category (Number): ").strip()
    if not cat.isdigit() or not 1 <= int(cat) <= len(CATEGORIES):
        print(" Invalid category selection!")
        logger.warning(f"User entered invalid category: {cat}")
        return
    category = CATEGORIES[int(cat)-1]
    logger.info(f"Category selected: {category}")

    # Amount input
    try:
        amount = float(input("Enter Amount: ").strip())
        logger.info(f"Amount entered: {amount}")
    except ValueError:
        print("Invalid amount!")
        logger.warning("User entered invalid amount")
        return

    # Show currencies
    for i, c in enumerate(CURRENCIES, 1):
        print(f"{i}. {c}")
    
    cur = input("Select Currency (Number): ").strip()
    if not cur.isdigit() or not 1 <= int(cur) <= len(CURRENCIES):
        print("Invalid currency selection!")
        logger.warning(f"User entered invalid currency option: {cur}")
        return
    currency = CURRENCIES[int(cur)-1]
    logger.info(f"Currency selected: {currency}")

    # Get PKR conversion
    rate = get_pkr_rate(currency)
    if rate is None:
        print(" Exchange rate unavailable!")
        logger.error(f"Rate unavailable for currency: {currency}")
        return

    pkr_val = round(amount * rate, 2)
    logger.info(f"Converted {amount} {currency} to {pkr_val} PKR at rate {rate}")

    # Read existing expenses
    data = read_json(JSON_FILE, DEFAULT_DATA)

    # Append new expense
    data["expenses"].append({
        "category": category,
        "amount": amount,
        "currency": currency,
        "amount_in_PKR": pkr_val
    })
    data["total"] = round(sum(e["amount_in_PKR"] for e in data["expenses"]), 2)

    # Write to JSON
    write_json(JSON_FILE, data)
    logger.info(f"Expense saved successfully: {category}, {amount} {currency}, {pkr_val} PKR")

    print(f" :) Success! Saved as {pkr_val} PKR")

# ---------------------- View Report ----------------------
def view_report():
    logger.info("User selected: View Expense Report")
    data = read_json(JSON_FILE, DEFAULT_DATA)

    print(f"\n{'Category':<10} | {'Amount':<15} | {'PKR Value'}")
    print("-" * 40)
    for e in data["expenses"]:
        print(f"{e['category']:<10} | {e['amount']:>6} {e['currency']:<7} | {e['amount_in_PKR']} PKR")
    print("-" * 40)
    print(f"TOTAL EXPENSES: {data['total']} PKR")
    logger.info(f"Displayed expense report. Total: {data['total']} PKR")
