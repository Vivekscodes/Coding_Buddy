#!/usr/bin/env python3
"""
Database migration script to handle schema changes for anonymous submissions
"""

import os
from flask import Flask
from models.database import db
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    """Drop and recreate database with updated schema"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///learning_recommender.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Check if database file exists
        db_path = 'learning_recommender.db'
        if os.path.exists(db_path):
            print(f"🗑️  Removing existing database: {db_path}")
            os.remove(db_path)
        
        print("🔨 Creating new database with updated schema...")
        db.create_all()
        print("✅ Database migration completed successfully!")
        print("📝 Schema changes:")
        print("   - Submission.user_id is now nullable (supports anonymous submissions)")
        print("   - Updated repr methods to handle anonymous users")

if __name__ == "__main__":
    migrate_database()
