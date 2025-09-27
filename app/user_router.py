from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm as FastAPIForm

# Importing core FastAPI components and utilities
from app.database import get_db
# 💥 FIX: Directly import the required schema classes to bypass potential caching issues
from app.schemas import User, UserCreate, Token 

from app.utils.auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user_from_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Correct model import path for your structure
from app.models.user import User as DBUser # Renamed to avoid conflict with schema.User

# Initialize the router
router = APIRouter(
    prefix="/users",
    tags=["Authentication & Users"],
)

# --- DEPENDENCY: Get Current User ---
# Must use the database model alias (DBUser) here
CurrentUser = Annotated[DBUser, Depends(get_current_user_from_token)]

# ----------------------------------------------------------------------
# WEEK 3/4: AUTHENTICATION AND USER MANAGEMENT
# ----------------------------------------------------------------------

@router.post("/register/", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Registers a new user."""
    # Check if user already exists
    if db.query(DBUser).filter(DBUser.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Hash the password (implementation assumed in utils.auth for this step)
    hashed_password = user.password + "notreallyhashed" # Placeholder for actual hashing
    
    # Create the user object (using the database model DBUser)
    db_user = DBUser(
        username=user.username, 
        email=user.email,
        hashed_password=hashed_password,
        granma_mode=user.granma_mode
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token/", response_model=Token) # Use the directly imported Token schema
def login_for_access_token(form_data: Annotated[FastAPIForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    """Generates a JWT token for a user after successful login."""
    
    # Authenticate user 
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=User) # Use the directly imported User schema
def read_users_me(current_user: CurrentUser):
    """Retrieves the details of the currently logged-in user."""
    return current_user