#!/bin/bash

# Railway Deployment Setup Script
echo "🚀 Starting Railway deployment setup..."

# Step 1: Health check
echo "🔍 Running database health check..."
python railway_health_check.py

if [ $? -ne 0 ]; then
    echo "❌ Database health check failed"
    exit 1
fi

# Step 2: Run migrations
echo "🔧 Running database migrations..."
python manage_db.py create-tables

# Step 3: Seed database if empty
echo "📊 Checking if database needs seeding..."
python railway_seed.py

# Step 4: Start the application
echo "🎯 Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
