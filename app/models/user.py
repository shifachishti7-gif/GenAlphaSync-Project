from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base # Import Base from the setup file

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    granma_mode = Column(Boolean, default=False)
    
    # Relationship to MoodEntry (defined in app/models/mood.py)
    # Use the string name "MoodEntry" because it's defined in a different file
    mood_entries = relationship("MoodEntry", back_populates="owner")