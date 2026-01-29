import streamlit as st
import pandas as pd
from services.expense_service import CATEGORIES, CURRENCIES, JSON_FILE, DEFAULT_DATA
from services.currency_service import get_pkr_rate, view_all_rates
from services.file_service import read_json, write_json
from logger_config import logger

st.set_page_config(page_title="Expense Tracker Pro", page_icon="💰")

def init_streamlit_files():
    """Ensure data files exist for the cloud environment."""
    data = read_json(JSON_FILE, DEFAULT_DATA)
    if not data["expenses"]:
        write_json(JSON_FILE, DEFAULT_DATA)

init_streamlit_files()

st.title("💰 Expense Tracker Pro")
st.markdown("Track your expenses in multiple currencies with live PKR conversion.")

# Sidebar Navigation
menu = ["Add Expense", "View Report", "Exchange Rates"]
choice = st.sidebar.selectbox("Menu", menu)

# --- ADD EXPENSE ---
if choice == "Add Expense":
    st.header("Add New Expense")
    
    with st.form("expense_form"):
        category = st.selectbox("Select Category", CATEGORIES)
        amount = st.number_input("Enter Amount", min_value=0.0, step=0.01)
        currency = st.selectbox("Select Currency", CURRENCIES)
        submit = st.form_submit_button("Save Expense")

        if submit:
            if amount > 0:
                rate = get_pkr_rate(currency)
                if rate:
                    pkr_val = round(amount * rate, 2)
                    data = read_json(JSON_FILE, DEFAULT_DATA)
                    
                    new_expense = {
                        "category": category,
                        "amount": amount,
                        "currency": currency,
                        "amount_in_PKR": pkr_val
                    }
                    data["expenses"].append(new_expense)
                    data["total"] = round(sum(e["amount_in_PKR"] for e in data["expenses"]), 2)
                    
                    write_json(JSON_FILE, data)
                    st.success(f"Saved! {amount} {currency} converted to {pkr_val} PKR")
                    logger.info(f"Streamlit: Saved {category} expense of {pkr_val} PKR")
                else:
                    st.error("Could not fetch exchange rate.")
            else:
                st.warning("Please enter an amount greater than 0.")

# --- VIEW REPORT ---
elif choice == "View Report":
    st.header("Expense Report")
    data = read_json(JSON_FILE, DEFAULT_DATA)
    
    if data["expenses"]:
        df = pd.DataFrame(data["expenses"])
        # Renaming for better display
        df.columns = ["Category", "Amount", "Currency", "PKR Value"]
        st.table(df)
        
        st.metric("Total Expenses (PKR)", f"{data['total']:,} PKR")
        
        if st.button("Clear All Records"):
            write_json(JSON_FILE, DEFAULT_DATA)
            st.rerun()
    else:
        st.info("No expenses recorded yet.")

# --- EXCHANGE RATES ---
elif choice == "Exchange Rates":
    st.header("Live Exchange Rates (to PKR)")
    rates_data = []
    for curr in CURRENCIES:
        rate = get_pkr_rate(curr)
        rates_data.append({"Currency": curr, "Rate (1 Unit to PKR)": rate})
    
    st.table(pd.DataFrame(rates_data))