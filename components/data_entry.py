"""
Data entry form component for expense tracker
"""
import streamlit as st
from datetime import datetime
from config import CATEGORIES, MIN_DATE, MAX_DATE
from database import db_manager
from utils import format_amount, validate_date

def render_data_entry_form():
    """
    Render the data entry form for adding expenses
    """
    st.markdown("### 📝 Add New Expense")
    
    # Create three columns for the form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category = st.selectbox(
            "Category",
            options=CATEGORIES,
            key="expense_category"
        )
    
    with col2:
        amount = st.number_input(
            "Amount Spent ($)",
            min_value=0.00,
            step=0.01,
            format="%.2f",
            key="expense_amount"
        )
    
    with col3:
        expense_date = st.date_input(
            "Date",
            min_value=MIN_DATE,
            max_value=MAX_DATE,
            value=datetime.now().date(),
            format="MM/DD/YYYY",
            key="expense_date"
        )
    
    # Submit button
    if st.button("Save Expense", type="primary",  width='stretch'):
        handle_form_submission(category, amount, expense_date)

def handle_form_submission(category: str, amount: float, expense_date):
    """
    Handle form submission and display appropriate messages
    
    Args:
        category: Selected category
        amount: Expense amount
        expense_date: Date of expense
    """
    # Format amount to 2 decimal places
    formatted_amount = format_amount(amount)
    
    # Validate date
    is_valid_date, error_msg = validate_date(expense_date)
    
    if not is_valid_date:
        st.error(f"❌ {error_msg}")
        return
    
    # Insert into database
    success, message = db_manager.insert_expense(
        category=category,
        amount=formatted_amount,
        expense_date=expense_date
    )
    
    if success:
        st.success(f"✅ {message}")
        st.balloons()
    else:
        if "Already recorded" in message:
            st.warning(f"⚠️ {message}")
        else:
            st.error(f"❌ {message}")