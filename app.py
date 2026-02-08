import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="SpendWise | Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# File to store data persistently
DATA_FILE = "expense_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Initialize data
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Sidebar - Budget Settings
with st.sidebar:
    st.header("⚙️ Settings")
    budget = st.number_input("Monthly Budget (₹)", min_value=0, value=2000)
    threshold = st.slider("Alert Threshold (%)", 50, 100, 80)
    st.markdown("---")
    st.info("Developed by [Sahil Parvez]")

st.title("💰 SpendWise")
st.markdown("*Keep your finances in check, one entry at a time.*")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("➕ Add Expense")
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.today())
        # Added more categories to make it professional
        cat = st.selectbox("Category", ["Food", "Travel", "Rent", "Shopping", "Misc"])
        amt = st.number_input("Amount (₹)", min_value=0.0)
        desc = st.text_input("Description")
        
        if st.form_submit_button("Log Expense"):
            if amt > 0 and desc:
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, amt, desc]], 
                                     columns=['Date', 'Category', 'Amount', 'Description'])
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                save_data(st.session_state.df)
                st.success("Expense logged!")
                st.rerun()

with col2:
    st.subheader("📊 Overview")
    df = st.session_state.df
    if not df.empty:
        total = df['Amount'].sum()
        remaining = budget - total
        used_pct = (total / budget) * 100

        m1, m2, m3 = st.columns(3)
        m1.metric("Spent", f"₹{total:,.0f}")
        m2.metric("Remaining", f"₹{remaining:,.0f}")
        m3.metric("Usage", f"{used_pct:.1f}%")

        if used_pct >= threshold:
            st.warning(f"⚠️ Budget Alert: You've used {used_pct:.1f}% of your limit!")

        # Charts
        fig = px.pie(df, values='Amount', names='Category', hole=0.4, title="Spending by Category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet. Start by adding an expense!")

st.markdown("---")
st.subheader("📋 History")

st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)

