# SQLAlchemy Model for Alert Tracking
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base # Ensure this Base import is correct
from app.schemas import AlertSeverity, AlertStatus # Import Enums from schemas

class DBAlert(Base):
    """
    Database model for storing CrisisAlerts triggered by users.
    The class name is explicitly set to DBAlert.
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    triggered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Store enums using SQLAlchemy's String type
    severity = Column(String, default=AlertSeverity.LOW.value, nullable=False)
    status = Column(String, default=AlertStatus.PENDING.value, nullable=False)
    is_resolved = Column(Boolean, default=False, nullable=False)
    
    # Text fields for administrative follow-up
    details = Column(String, nullable=True) 
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(String, nullable=True)

    # Define relationship back to the User model using the correct class name string "User"
    owner = relationship("User", back_populates="alerts")
