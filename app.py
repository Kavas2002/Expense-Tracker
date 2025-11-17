from azure.storage.blob import BlobServiceClient
import streamlit as st
import pandas as pd
from datetime import date
import io

# AZURE CONNECTION PARAMETER

AZURE_CONNECTION_STRING = st.secrets["AZURE_CONNECTION_STRING"]
CONTAINER_NAME = st.secrets["CONTAINER_NAME"]
BLOB_NAME = st.secrets["BLOB_NAME"]

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
blob_client = container_client.get_blob_client(BLOB_NAME)

# LOAD CSV FROM AZURE
def load_csv_from_azure():
    try:
        stream = io.BytesIO()
        blob_client.download_blob().readinto(stream)
        stream.seek(0)
        df = pd.read_csv(stream)
        return df
    except Exception:
        return pd.DataFrame({
            "Date": [],
            "Category": [],
            "Description": [],
            "Payment Method": [],
            "Amount": [],
            "Notes": []
        })

# Upload CSV to Azure
def upload_csv_to_azure(df):
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    blob_client.upload_blob(stream.getvalue(), overwrite=True)

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = load_csv_from_azure()

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
            
            upload_csv_to_azure(st.session_state["expenses"])

            st.success("Expense added successfully and saved to CSV!")

# Display Expenses
st.subheader("📄 All Expenses")
st.dataframe(st.session_state["expenses"], use_container_width=True)

