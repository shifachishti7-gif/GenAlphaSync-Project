import uvicorn
from fastapi import FastAPI
from app.database import create_all_tables
from app.user_router import router as user_router
from app.mood_router import router as mood_router

# CRITICAL FIX: Ensure models are loaded before table creation.
# By importing the model files here, SQLAlchemy registers the tables with Base.metadata.
# NOTE: We do NOT need to import "from app.models import __init__" because the other imports handle it.
from app.models import user, mood 


# Initialize FastAPI app
app = FastAPI(
    title="GenAlphaSync Backend API",
    description="API for user authentication, mood tracking, and crisis detection.",
    version="1.0.0",
)

# Application startup event handler
@app.on_event("startup")
def startup_event():
    print("Initializing database...")
    # This checks all classes that inherited from Base (User, MoodEntry)
    # and creates the tables if they don't exist.
    create_all_tables()
    print("Database initialization complete.")

# Include the routers
app.include_router(user_router)
app.include_router(mood_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)