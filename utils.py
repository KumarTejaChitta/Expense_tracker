"""
Utility functions for data validation and formatting
"""
from datetime import datetime, date
from typing import Optional, Tuple
from config import MIN_DATE, MAX_DATE

def format_amount(amount: float) -> float:
    """
    Format amount to 2 decimal places
    
    Args:
        amount: Input amount
        
    Returns:
        Float rounded to 2 decimal places
    """
    return round(float(amount), 2)

def validate_date(selected_date: date) -> Tuple[bool, str]:
    """
    Validate if date is within acceptable range
    
    Args:
        selected_date: Date to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if selected_date < MIN_DATE:
        return False, f"Date cannot be before {MIN_DATE.strftime('%m/%d/%Y')}"
    
    if selected_date > MAX_DATE:
        return False, "Date cannot be in the future"
    
    return True, ""

def format_date_display(date_value: date) -> str:
    """
    Format date for display in MM/DD/YYYY format
    
    Args:
        date_value: Date to format
        
    Returns:
        Formatted date string
    """
    return date_value.strftime("%m/%d/%Y")