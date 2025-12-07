"""
Configuration settings for the Expense Tracker application
"""
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'expense_tracker'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Application Constants
CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Health", "Other"]

# Date Configuration
MIN_YEAR = 2023
MIN_DATE = datetime(MIN_YEAR, 1, 1).date()
MAX_DATE = datetime.now().date()

# UI Configuration
PAGE_TITLE = "Simple Expense Tracker"
PAGE_ICON = "💰"
LAYOUT = "wide"