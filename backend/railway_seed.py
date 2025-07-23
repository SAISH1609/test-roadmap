#!/usr/bin/env python3
"""
Railway deployment data seeder
This script will seed the database with initial data for Railway deployment
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def seed_database():
    """Seed the database with initial roadmap data"""
    if not DATABASE_URL:
        print("Error: DATABASE_URL environment variable not set")
        return False
    
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as db:
            # Check if data already exists
            result = db.execute(text("SELECT COUNT(*) FROM roadmap_topics"))
            count = result.scalar()
            
            if count > 0:
                print(f"Database already has {count} records. Skipping seed.")
                return True
            
            print("Seeding database with initial data...")
            
            # Insert sample roadmaps
            roadmaps_sql = """
            INSERT INTO roadmaps (id, name, description, created_at, updated_at) VALUES
            (1, 'SQL', 'Learn SQL and databases', NOW(), NOW()),
            (2, 'React', 'Learn React development', NOW(), NOW()),
            (3, 'Python', 'Learn Python programming', NOW(), NOW())
            ON CONFLICT (id) DO NOTHING;
            """
            
            db.execute(text(roadmaps_sql))
            
            # Insert sample topics (subset of your data)
            topics_sql = """
            INSERT INTO roadmap_topics (id, roadmap_id, name, description, x, y, width, height, is_completed, created_at) VALUES
            (1, 1, 'Learn the Basics', 'Introduction to SQL fundamentals', NULL, NULL, 5, 1, true, NOW()),
            (2, 1, 'What Are Relational Databases?', 'Understanding relational database concepts', NULL, NULL, 1, 1, true, NOW()),
            (31, 2, 'CLI Tools', 'React development tools', NULL, NULL, NULL, 1, true, NOW()),
            (56, 3, 'Learn the Basics', 'Python programming fundamentals', NULL, NULL, NULL, 1, true, NOW())
            ON CONFLICT (id) DO NOTHING;
            """
            
            db.execute(text(topics_sql))
            db.commit()
            
            print("Database seeded successfully!")
            return True
            
    except Exception as e:
        print(f"Error seeding database: {e}")
        return False

if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
