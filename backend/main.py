from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os

from app.database import get_db
from app.routers import auth, roadmaps, teams, users, progress, admin, activity
from app.models import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Roadmap.sh Clone API",
    description="Backend API for roadmap.sh platform",
)

# Updated CORS for Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "https://*.railway.app",  # Allow Railway frontend domains
        "https://*.up.railway.app",  # Allow Railway frontend domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roadmaps.router, prefix="/api/roadmaps", tags=["Roadmaps"])
app.include_router(teams.router, prefix="/api/teams", tags=["Teams"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(activity.router, prefix="/api/activity", tags=["Activity"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
def read_root():
    return {"message": "Roadmap.sh Clone API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running", "cors": "enabled"}


@app.get("/cors-test")
def cors_test():
    return {"message": "CORS is working!", "origin": "allowed"}


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    """Test database connection and attempt to seed data if empty"""
    try:
        from sqlalchemy import text

        # Test connection
        db.execute(text("SELECT 1"))

        # Check tables and counts
        tables_status = {}

        # Check roadmaps
        try:
            result = db.execute(text("SELECT COUNT(*) FROM roadmaps"))
            roadmap_count = result.scalar()
            tables_status["roadmaps_count"] = roadmap_count

            if roadmap_count == 0:
                # Try to insert sample data
                db.execute(text("""
                    INSERT INTO roadmaps (id, name, description, created_at, updated_at) VALUES
                    (1, 'SQL', 'Learn SQL and databases', NOW(), NOW()),
                    (2, 'React', 'Learn React development', NOW(), NOW()),
                    (3, 'Python', 'Learn Python programming', NOW(), NOW())
                    ON CONFLICT (id) DO NOTHING;
                """))
                db.commit()
                tables_status["roadmaps_seeded"] = "Attempted"
        except Exception as e:
            tables_status["roadmaps_error"] = str(e)

        # Check roadmap_topics
        try:
            result = db.execute(text("SELECT COUNT(*) FROM roadmap_topics"))
            topics_count = result.scalar()
            tables_status["topics_count"] = topics_count

            if topics_count == 0:
                # Try to insert sample topics
                db.execute(text("""
                    INSERT INTO roadmap_topics (id, roadmap_id, name, description, width, height, is_completed, created_at) VALUES
                    (1, 1, 'Learn the Basics', 'Introduction to SQL fundamentals', 5, 1, true, NOW()),
                    (2, 1, 'What Are Relational Databases?', 'Understanding relational database concepts', 1, 1, true, NOW()),
                    (31, 2, 'CLI Tools', 'React development tools', NULL, 1, true, NOW()),
                    (56, 3, 'Learn the Basics', 'Python programming fundamentals', NULL, 1, true, NOW())
                    ON CONFLICT (id) DO NOTHING;
                """))
                db.commit()
                tables_status["topics_seeded"] = "Attempted"
        except Exception as e:
            tables_status["topics_error"] = str(e)

        return {
            "status": "success",
            "message": "Database test completed",
            "tables": tables_status
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
