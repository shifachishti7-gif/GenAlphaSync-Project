from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base # Import Base from app/models/__init__.py

class MoodEntry(Base):
    """
    SQLAlchemy model representing a single mood entry recorded by a user.
    This defines the columns for the 'mood_entries' database table.
    """
    __tablename__ = "mood_entries"

    # Columns
    id = Column(Integer, primary_key=True, index=True)
    mood = Column(String, index=True, nullable=False) # e.g., "Happy", "Stressed"
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key: This links the mood entry back to the user who created it
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to the User model
    owner = relationship("User", back_populates="mood_entries")

    def __repr__(self):
        return f"<MoodEntry(id={self.id}, mood='{self.mood}', owner_id={self.owner_id})>"
