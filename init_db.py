#!/usr/bin/env python3
"""
Database initialization script for Court Data Fetcher
"""

from app import create_app, db

def init_database():
    """Initialize the database with required tables"""
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        print("📊 Tables created:")
        print("   - query_log")

if __name__ == "__main__":
    init_database() 