#!/bin/bash

# Railway startup script for backend
echo "Starting Railway deployment..."

# Check if database connection is available
echo "Checking database connection..."
python manage_db.py check-connection

# Create tables if needed
echo "Creating tables if needed..."
python manage_db.py create-tables

# Check if we need to load initial data
echo "Checking if data needs to be loaded..."
if python manage_db.py check-data-exists | grep -q 'Found 0 records'; then
    echo "Loading initial data from SQL file..."
    # Note: For Railway, we'll need to handle this differently
    # as we won't have the SQL file in the deployment
    echo "Skipping SQL import for Railway deployment - will use API to seed data"
else
    echo "Data already exists, skipping data load"
fi

# Start the application
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port $PORT
