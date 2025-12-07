from database import db_manager

# Test connection
conn = db_manager.connect()
if conn:
    print("✅ Database connection successful!")
    db_manager.close()
else:
    print("❌ Database connection failed. Check your credentials in .env file")