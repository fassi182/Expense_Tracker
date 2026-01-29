# EXPENSE TRACKER 

## What the Project Is
Expense Tracker  is a Python app to track expenses in multiple currencies, convert them to PKR, and maintain persistent records. It is modular, maintainable, and suitable for personal or business use.

## Problem It Solves
Manually tracking foreign currency expenses is error-prone. This app:
- Converts foreign amounts to PKR by calling the Fawaz Ahmed Currency API(used stored exchange rates if API fail/offline).
- Keeps persistent expense records.
- Provides quick reports and totals.
- Logs all actions for auditing and debugging.

## Folder Structure

```
expense_tracker/
|
- app.py                 # Main entry point
- streamlit_App.txt
- requirements.txt
- logger_config.py       # Logging setup
- README.md              # Documentation file
- data/
  - expenses.json        # Stores expenses
  - rates_cache.json     # Caches currency rates
- services/
  - file_service.py      # Handles JSON read/write
  - expense_service.py   # Adds expenses, converts currency, updates totals
  - currency_service.py  # Fetches live currency rates, shows table
- .gitignore
```
# Expense Tracker - How It Works

## Startup

* Ensures `data/` and `logs/` folders exist.
* Creates `expenses.json` or `rates_cache.json` with default values if missing.
* Initializes logger to write all events and errors to `logs/app.log`.

## Main Menu

The user sees options:

* Add Expense
* View Report
* View Exchange Rates
* Exit

## Adding Expense

* User selects a category from a numbered list.
* User enters the amount spent.
* User selects the currency from a numbered list.
* The app fetches the PKR conversion rate from API or cache.
* Expense is saved in `expenses.json` with both original and PKR values.
* Total expense in PKR is updated.

## Viewing Report

* Reads `expenses.json` and displays all expenses in a tabular format.
* Shows category, amount, currency, PKR value, and total PKR spent.

## Viewing Exchange Rates

* Fetches rates for all supported currencies to PKR.
* Uses cached rates from `rates_cache.json` if offline.
* Displays the rates in a formatted table.

## Logging

* Logs every action, API call, and error in `logs/app.log`.

## Exit

* Exits cleanly.
* All data remains persistent in JSON files.

## Skills Used
- Python 3.x, OOP, modular programming
- JSON handling and file I/O
- Logging and error management
- API integration and calculations

## Tools Used
- `requests` library for currency rates
- Python standard library (`os`, `json`, `logging`)
- Terminal or command line to run the app
