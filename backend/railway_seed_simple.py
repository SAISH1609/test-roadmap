#!/usr/bin/env python3
"""
Railway deployment data seeder - Simplified version
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def seed_database():
    """Seed the database with initial roadmap data"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("[SEED] Error: DATABASE_URL environment variable not set")
        return True  # Don't fail deployment
    
    try:
        print("[SEED] Connecting to database...")
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        with SessionLocal() as db:
            # Check if data already exists
            print("[SEED] Checking for existing data...")
            try:
                result = db.execute(text("SELECT COUNT(*) FROM roadmap_topics"))
                count = result.scalar()
                
                if count and count > 0:
                    print(f"[SEED] Database already has {count} records. Skipping seed.")
                    return True
            except:
                print("[SEED] Tables don't exist yet, continuing...")
            
            print("[SEED] Seeding database with initial data...")
            
            # Insert sample roadmaps
            try:
                roadmaps_sql = """
                INSERT INTO roadmaps (id, name, description, created_at, updated_at) VALUES
                (1, 'SQL', 'Learn SQL and databases', NOW(), NOW()),
                (2, 'React', 'Learn React development', NOW(), NOW()),
                (3, 'Python', 'Learn Python programming', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING;
                """
                db.execute(text(roadmaps_sql))
                db.commit()
                print("[SEED] Roadmaps seeded successfully!")
            except Exception as e:
                print(f"[SEED] Roadmaps seeding failed (might be normal): {e}")
            
            return True
            
    except Exception as e:
        print(f"[SEED] Database seeding failed: {e}")
        print("[SEED] Continuing deployment anyway...")
        return True  # Don't fail deployment

if __name__ == "__main__":
    success = seed_database()
    sys.exit(0)
