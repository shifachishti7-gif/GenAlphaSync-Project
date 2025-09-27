# This file imports all SQLAlchemy models so that they are registered 
# with the Base class from app.database before being used by the system.

# Import Base from the central database connection file (one level up)
from ..database import Base

# Import all models to link them to the Base class
from .user import User
from .mood import MoodEntry
from .alert import DBAlert # <-- Corrected import to use DBAlert
