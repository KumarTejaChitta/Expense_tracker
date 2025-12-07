"""
Database operations module for Expense Tracker
Handles all database connections and CRUD operations
"""
import pg8000
from pg8000.native import Connection
from datetime import datetime, date
from typing import Optional, List, Dict, Tuple
import pandas as pd
from config import DATABASE_CONFIG

class DatabaseManager:
    """Manages all database operations for the expense tracker"""
    
    def __init__(self):
        """Initialize database manager"""
        self.connection = None
        
    def connect(self) -> Optional[Connection]:
        """
        Establish database connection
        Returns: Connection object or None if connection fails
        """
        try:
            self.connection = pg8000.native.Connection(
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                database=DATABASE_CONFIG['database'],
                host=DATABASE_CONFIG['host'],
                port=int(DATABASE_CONFIG['port'])
            )
            return self.connection
        except Exception as e:
            print(f"Database connection failed: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def insert_expense(self, category: str, amount: float, expense_date: date) -> Tuple[bool, str]:
        """
        Insert a new expense into the database
        
        Args:
            category: Expense category
            amount: Amount spent (will be rounded to 2 decimal places)
            expense_date: Date of expense
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Round amount to 2 decimal places
            amount = round(float(amount), 2)
            
            # Connect to database
            if not self.connection:
                self.connect()
            
            # Check for duplicate entry
            check_query = """
                SELECT COUNT(*) FROM expenses 
                WHERE category = :category 
                AND amount = :amount 
                AND date = :date
            """
            result = self.connection.run(
                check_query,
                category=category,
                amount=amount,
                date=expense_date
            )
            
            if result[0][0] > 0:
                return False, "Already recorded"
            
            # Insert new expense
            insert_query = """
                INSERT INTO expenses (category, amount, date) 
                VALUES (:category, :amount, :date)
            """
            self.connection.run(
                insert_query,
                category=category,
                amount=amount,
                date=expense_date
            )
            
            return True, "Values recorded successfully"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_total_expense(self) -> float:
        """
        Get total of all expenses
        Returns: Total expense amount
        """
        try:
            if not self.connection:
                self.connect()
            
            query = "SELECT COALESCE(SUM(amount), 0) FROM expenses"
            result = self.connection.run(query)
            return float(result[0][0])
            
        except Exception as e:
            print(f"Error getting total expense: {e}")
            return 0.0

    def get_expenses_by_category(self) -> pd.DataFrame:
        """
        Get total expenses grouped by category
        Returns: DataFrame with category and total amount
        """
        try:
            if not self.connection:
                self.connect()
            
            query = """
                SELECT category, SUM(amount) as total 
                FROM expenses 
                GROUP BY category 
                ORDER BY total DESC
            """
            result = self.connection.run(query)
            
            if result:
                df = pd.DataFrame(result, columns=['Category', 'Total'])
                return df
            else:
                return pd.DataFrame(columns=['Category', 'Total'])
                
        except Exception as e:
            print(f"Error getting expenses by category: {e}")
            return pd.DataFrame(columns=['Category', 'Total'])

    def get_expense_trend(self) -> pd.DataFrame:
        """
        Get daily expense trends
        Returns: DataFrame with date and total amount per day
        """
        try:
            if not self.connection:
                self.connect()
            
            query = """
                SELECT date, SUM(amount) as daily_total 
                FROM expenses 
                GROUP BY date 
                ORDER BY date
            """
            result = self.connection.run(query)
            
            if result:
                df = pd.DataFrame(result, columns=['Date', 'Total'])
                df['Date'] = pd.to_datetime(df['Date'])
                return df
            else:
                return pd.DataFrame(columns=['Date', 'Total'])
                
        except Exception as e:
            print(f"Error getting expense trend: {e}")
            return pd.DataFrame(columns=['Date', 'Total'])
        
    def get_highest_lowest_category(self) -> Dict[str, Dict[str, float]]:
        """
        Get highest and lowest spending categories
        Returns: Dictionary with highest and lowest category details
        """
        try:
            if not self.connection:
                self.connect()
            
            query = """
                SELECT category, SUM(amount) as total 
                FROM expenses 
                GROUP BY category 
                ORDER BY total DESC
            """
            result = self.connection.run(query)
            
            if result and len(result) > 0:
                highest = {
                    'category': result[0][0],
                    'amount': float(result[0][1])
                }
                lowest = {
                    'category': result[-1][0],
                    'amount': float(result[-1][1])
                }
                return {
                    'highest': highest,
                    'lowest': lowest
                }
            else:
                return {
                    'highest': {'category': 'N/A', 'amount': 0.0},
                    'lowest': {'category': 'N/A', 'amount': 0.0}
                }
                
        except Exception as e:
            print(f"Error getting highest/lowest category: {e}")
            return {
                'highest': {'category': 'N/A', 'amount': 0.0},
                'lowest': {'category': 'N/A', 'amount': 0.0}
            }

# Create a singleton instance - THIS LINE IS IMPORTANT!
db_manager = DatabaseManager()