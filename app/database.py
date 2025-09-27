from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 1. Load config
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# 2. Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Only add connect_args if we are using SQLite
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# 3. SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base
Base = declarative_base()

# 5. Dependency Function
def get_db():
    """Provides a transactional database session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. Table Creation Function
def create_all_tables():
    """Creates all defined tables in the database.
       NOTE: The models (User, MoodEntry) are loaded via the app's structure
             before this function is called."""
    Base.metadata.create_all(bind=engine)