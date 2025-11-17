import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Daily Expenses Tracker", layout="wide")

st.title("💰 Daily Expenses Tracker")

# Initialize session state for storing expenses
def init_state():
    if "expenses" not in st.session_state:
        st.session_state["expenses"] = pd.DataFrame({
            "Date": [],
            "Category": [],
            "Description": [],
            "Payment Method": [],
            "Amount": [],
            "Notes": []
        })

init_state()

# Sidebar - Add new expense
st.sidebar.header("Add New Expense")

with st.sidebar.form("expense_form"):
    expense_date = st.date_input("Date", value=date.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Groceries", "Rent", "Bills", "Shopping", "Health", "Entertainment", "Others"],
    )
    description = st.text_input("Description")
    payment_method = st.selectbox(
        "Payment Method", ["Cash", "UPI", "Credit Card", "Debit Card", "Bank Transfer"]
    )
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    notes = st.text_area("Notes", height=70)

    confirm_add = st.checkbox("✔ Confirm to Add Expense")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if not confirm_add:
            st.warning("Please tick the checkbox to confirm adding the expense.")
        else:
            new_entry = pd.DataFrame({
                "Date": [expense_date],
                "Category": [category],
                "Description": [description],
                "Payment Method": [payment_method],
                "Amount": [amount],
                "Notes": [notes],
            })
            st.session_state["expenses"] = pd.concat([st.session_state["expenses"], new_entry], ignore_index=True)
                    # Save to CSV
            csv_path = "expenses.csv"
            try:
                # If file does not exist, write with header
                st.session_state["expenses"].to_csv(csv_path, index=False)
            except Exception as e:
                st.error(f"Error saving to CSV: {e}")

            st.success("Expense added successfully and saved to CSV!")

# Display Expenses
st.subheader("📄 All Expenses")
st.dataframe(st.session_state["expenses"], use_container_width=True)

