import streamlit as st
from datetime import date, time

st.title("Expense Tracker")
st.write(" Enter the details of the expense")


with st.form("Expense_form"):
    expense_date = st.date_input("date",date.today())
    category = st.selectbox()