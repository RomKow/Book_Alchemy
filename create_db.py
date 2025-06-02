"""
create_db.py

Creates the database tables for the Flask application.
Run this script once to initialize the SQLite database.
"""

from app import app
from data_models import db

# Use the Flask application context to create all tables
with app.app_context():
    db.create_all()
    print("Database tables have been created.")
