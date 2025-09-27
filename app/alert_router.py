# app/alert_router.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/alerts",
    tags=["Safety - Crisis Detection"],
)

class CrisisInput(BaseModel):
    user_id: int
    message: str

@router.post("/crisis/", status_code=status.HTTP_200_OK)
def detect_crisis_stub(data: CrisisInput):
    """
    Placeholder endpoint for the AI/ML Specialist to integrate 
    the crisis detection model. This currently simulates a result.
    """
    
    # Check for a crisis signal (stubbed logic)
    message_lower = data.message.lower()
    if "help" in message_lower or "crisis" in message_lower or "harm" in message_lower:
        risk_level = "HIGH"
        response_message = "RISK DETECTED. Tier 1 triage protocol initiated."
    else:
        risk_level = "LOW"
        response_message = "Risk check passed. Proceeding with conversation."
        
    return {
        "user_id": data.user_id,
        "status": response_message,
        "risk_level": risk_level,
        "timestamp": datetime.now().isoformat()
    }