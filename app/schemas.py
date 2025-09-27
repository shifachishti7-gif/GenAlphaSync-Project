from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum
from typing import List, Optional

# --- ENUMS (Breaking the Circular Dependency) ---
class AlertSeverity(str, Enum):
    """Defines the severity levels for a crisis alert."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AlertStatus(str, Enum):
    """Defines the resolution status for a crisis alert."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

# --- CORE SCHEMAS ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- MOOD SCHEMAS ---
class MoodEntryBase(BaseModel):
    mood: str = Field(..., description="The emotional state logged (e.g., 'Happy', 'Anxious').")
    
class MoodEntryCreate(MoodEntryBase):
    pass

class MoodEntry(MoodEntryBase):
    id: int
    owner_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# --- ALERT SCHEMAS ---
class Alert(BaseModel):
    id: int
    user_id: int
    triggered_at: datetime
    severity: AlertSeverity
    status: AlertStatus
    is_resolved: bool
    details: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None
    
    class Config:
        from_attributes = True

# --- ANALYTICS SCHEMAS (for Persona 6: Teacher Dashboard) ---
class MoodSummary(BaseModel):
    mood: str
    count: int

class MoodAnalytics(BaseModel):
    total_users_checked: int = Field(..., description="Total number of users registered.")
    total_moods_last_7_days: int = Field(..., description="Total entries logged in the past week.")
    most_common_moods: List[MoodSummary] = Field(..., description="Top 5 most frequent moods in the past week.")
    users_with_alerts_last_30_days: int = Field(..., description="Count of unique users who triggered a high-severity alert in the last month.")
