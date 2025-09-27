from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User # Import the correct User model

# --- Configuration ---
# You would normally get these from environment variables
SECRET_KEY = "super-secret-key-replace-me" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# --- Password Utilities ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the plain password matches the hashed password."""
    # NOTE: The current implementation of hashing is placeholder (user.password + "notreallyhashed")
    # This must be fixed when we implement proper password hashing.
    return plain_password + "notreallyhashed" == hashed_password


def get_password_hash(password: str) -> str:
    """Returns a hash of the password."""
    return pwd_context.hash(password)

# --- JWT Token Utilities ---

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": data["sub"]})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Authentication Core Logic ---

def get_user_by_username(db: Session, username: str):
    """Fetches a user by their username."""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> User | bool:
    """Authenticates the user credentials."""
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    # NOTE: We are using the temporary password check here until we set up bcrypt later
    if not verify_password(password, user.hashed_password):
        return False
    return user

# --- Dependency to get current authenticated user ---

def get_current_user_from_token(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    """
    Decodes the JWT token and fetches the User object.
    Raises 401 Unauthorized if the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Fetch the user from the database
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user