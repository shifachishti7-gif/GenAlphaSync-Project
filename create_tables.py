# create_tables.py

import sys
# Allows import app.* to work from the project root
sys.path.append('app') 

from app.database import engine, Base
# Import all models so Base knows about them
from app.models.user import User
from app.models.mood import Mood

def create_database_tables():
    """Initializes the database schema."""
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_database_tables()