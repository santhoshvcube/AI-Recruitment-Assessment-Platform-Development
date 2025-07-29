from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional

from app.models.user_models import User, FreeTrialUser
from app.models.schemas import FreeTrialUserCreate, Token
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Mock database for demonstration purposes
mock_free_trial_users = {}

@router.post("/register", response_model=Token)
async def register_free_trial_user(user: FreeTrialUserCreate):
    if user.email in mock_free_trial_users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Simulate user creation and trial activation
    trial_end_time = datetime.utcnow() + timedelta(hours=1) # 1 hour free trial
    new_user = FreeTrialUser(
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.password, # In a real app, hash this password
        trial_start_time=datetime.utcnow(),
        trial_end_time=trial_end_time
    )
    mock_free_trial_users[user.email] = new_user

    # Generate a mock token
    access_token_expires = timedelta(minutes=60) # Token valid for 1 hour
    access_token = "mock_free_trial_token"
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login_free_trial_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = mock_free_trial_users.get(form_data.username)
    if not user or user.hashed_password != form_data.password: # In real app, verify hashed password
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    if datetime.utcnow() > user.trial_end_time:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Free trial has expired")

    # Generate a mock token
    access_token_expires = timedelta(minutes=60)
    access_token = "mock_free_trial_token"
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/status")
async def get_free_trial_status(current_user: FreeTrialUser = Depends()): # This would require a proper dependency for current user
    if datetime.utcnow() > current_user.trial_end_time:
        return {"status": "expired", "time_remaining": 0}
    
    time_remaining = (current_user.trial_end_time - datetime.utcnow()).total_seconds()
    return {"status": "active", "time_remaining": time_remaining}


