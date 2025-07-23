#!/usr/bin/env python3
"""
Database migration and health check for Railway deployment
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def check_database_health():
    """Check database connection and table structure"""
    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL environment variable not set")
        return False
    
    try:
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Check if tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['roadmaps', 'roadmap_topics', 'users', 'teams', 'user_progress']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {missing_tables}")
            print("🔧 Creating missing tables...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tables created successfully")
        else:
            print("✅ All required tables exist")
        
        return True
        
    except Exception as e:
        print(f"❌ Database health check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Running Railway database health check...")
    success = check_database_health()
    
    if success:
        print("🎉 Database is ready for Railway deployment!")
    else:
        print("💥 Database health check failed!")
        
    sys.exit(0 if success else 1)
