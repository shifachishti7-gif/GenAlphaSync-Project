from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import datetime, timedelta, timezone
from typing import List
from app.models.user import User as DBUser
from app.dependencies import get_db, get_current_user_from_token
from app.models.mood import MoodEntry as DBMoodEntry
from app.models.alert import DBAlert
from app.schemas import (
    User, 
    MoodEntryCreate, 
    MoodEntry, 
    MoodAnalytics, 
    MoodSummary
)

router = APIRouter(prefix="/moods", tags=["Mood Tracking"])
# --- Endpoint 1: Create Mood Entry (POST /moods/) ---
@router.post(
    "/",
    response_model=MoodEntry,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new personal mood entry"
)
def create_mood_entry(
    mood_data: MoodEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Allows an authenticated user to log their current emotional state.
    """
    new_entry = DBMoodEntry(
        owner_id=current_user.id,
        mood=mood_data.mood,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


# --- Endpoint 2: Read User Mood History (GET /moods/) ---
@router.get(
    "/",
    response_model=List[MoodEntry],
    summary="Retrieve personal mood history"
)
def read_mood_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Fetches all mood entries logged by the currently authenticated user, ordered by most recent.
    """
    entries = db.query(DBMoodEntry).filter(
        DBMoodEntry.owner_id == current_user.id
    ).order_by(
        DBMoodEntry.timestamp.desc()
    ).all()
    
    return entries
# --- Endpoint 3: Analytics for Teacher Dashboard (GET /moods/analytics/mood_summary/) ---
@router.get(
    "/analytics/mood_summary/",
    response_model=MoodAnalytics,
    summary="Teacher Dashboard Analytics Summary",
    description="Analytic data summary for the teacher dashboard"
)
def get_mood_analytics(
    db: Session = Depends(get_db),
    # NOTE: Add teacher authorization dependency here in a real deployment
    current_user: User = Depends(get_current_user_from_token) 
):
    """
    Calculates key metrics for the administrative or teacher dashboard. 
    Metrics include overall user count, recent activity, top moods, and recent crisis alerts.
    """
    now = datetime.now(timezone.utc)
    date_7_days_ago = now - timedelta(days=7)
    date_30_days_ago = now - timedelta(days=30)
# 1. Total Number of Users
    total_users_checked = db.query(DBUser).count()

    # 2. Total Mood Entries Logged in the Last 7 Days
    total_moods_last_7_days = db.query(DBMoodEntry).filter(
        DBMoodEntry.timestamp >= date_7_days_ago
    ).count()

    # 3. Top 5 Most Common Moods in the Last 7 Days
    top_moods_results = db.query(
        DBMoodEntry.mood,
        func.count(DBMoodEntry.mood).label('mood_count')
    ).filter(
        DBMoodEntry.timestamp >= date_7_days_ago
    ).group_by(DBMoodEntry.mood).order_by(
        func.count(DBMoodEntry.mood).desc()
    ).limit(5).all()

    # Map query results to MoodSummary schema
    most_common_moods = [
        MoodSummary(mood=mood, count=count) for mood, count in top_moods_results
    ]

    # 4. Number of Unique Users with a CrisisAlert in the Last 30 Days
    users_with_alerts_last_30_days = db.query(
        func.count(distinct(DBAlert.user_id))
    ).filter(
        DBAlert.triggered_at >= date_30_days_ago
    ).scalar()

    return MoodAnalytics(
        total_users_checked=total_users_checked,
        total_moods_last_7_days=total_moods_last_7_days,
        most_common_moods=most_common_moods,
        users_with_alerts_last_30_days=users_with_alerts_last_30_days
    )