# tests/test_users.py (THE FINAL, SYNCHRONOUS, WORKING VERSION)

import pytest
# CHANGE 1: Import the standard synchronous TestClient from FastAPI's utilities
from fastapi.testclient import TestClient
from main import app 

# Instantiate the TestClient once with your main FastAPI application
client = TestClient(app)

# CHANGE 2: Define tests as standard Python functions (no 'async' needed)
def test_read_root():
    """Tests the basic root endpoint."""
    # CHANGE 3: Call the synchronous client instance
    response = client.get("/") 
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to GenAlphaSync API! Ready for the next steps."}

# CHANGE 2: Define tests as standard Python functions (no 'async' needed)
def test_register_and_login_user():
    """Tests the entire user lifecycle: registration followed by login."""
    
    # ---------------------------------
    # 1. TEST USER REGISTRATION
    # ---------------------------------
    register_data = {
        "username": "testuser",
        "email": "test-final@example.com", # Use a unique email to ensure the test works every time
        "password": "securepassword123",
        "granma_mode": False
    }
    
    # CHANGE 3: Call the synchronous client instance
    response = client.post("/users/", json=register_data)
    
    # Expect successful creation (201)
    assert response.status_code == 201
    
    response_data = response.json()
    assert response_data["message"] == "User registered successfully"
    assert "user_id" in response_data
    
    # ---------------------------------
    # 2. TEST USER LOGIN
    # ---------------------------------
    login_data = {
        "email": "test-final@example.com",
        "password": "securepassword123"
    }
    
    # CHANGE 3: Call the synchronous client instance
    response = client.post("/users/login", json=login_data)
    
    # Expect successful login (200)
    assert response.status_code == 200
    
    login_response = response.json()
    assert "access_token" in login_response
    assert login_response["token_type"] == "bearer"
    assert "user_id" in login_response