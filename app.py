import streamlit as st
from datetime import datetime,date
import pandas as pd

st.title("Expense Tracker")
st.write(" Enter the details of the expense")


with st.form("Expense_form"):
    expense_date = st.date_input("date",date.today())
    expense_time = st.time_input("Time",datetime.now().time())
    category = st.selectbox("Select the category of expense",["Personal","Business","Friend","Debt","Other"])
    amount = st.number_input("Enter the Spent amount",min_value=0.0,format="%.2f")
    Descrition = st.text_input("enter the Product/Service description")
    localtion = st.text
    
    checkbox = st.checkbox("confirm expense")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if checkbox:
            st.success("expense recorded successfully")
            Expense_data={
                "Date":expense_date,
                "Time":expense_time,
                "Category":category,
                "Amount":amount,
                "Description":Descrition
            }
        else:
            st.warring("please confirm the checkbox")
        
