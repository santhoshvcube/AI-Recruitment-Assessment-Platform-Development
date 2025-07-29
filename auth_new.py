from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic import BaseModel, EmailStr, validator
import re

from app.db.session import get_db
from app.models.user_models import User, Student, Admin
from app.models.schemas import Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT Configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic models for requests
class StudentRegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    mobile_number: str
    student_id: Optional[str] = None
    course: Optional[str] = None
    year_of_study: Optional[str] = None
    college: Optional[str] = None
    
    @validator('mobile_number')
    def validate_mobile(cls, v):
        if not Student.validate_mobile_number(v):
            raise ValueError('Invalid mobile number format')
        return v

class StudentLoginRequest(BaseModel):
    email: EmailStr
    password: str  # Initially mobile number

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return payload
    except jwt.PyJWTError:
        raise credentials_exception

@router.post("/student/register", response_model=dict)
async def register_student(
    student_data: StudentRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new student"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == student_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if mobile number already exists
    existing_student = db.query(Student).filter(Student.mobile_number == student_data.mobile_number).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )
    
    # Create user with mobile number as initial password
    hashed_password = User.hash_password(student_data.mobile_number)
    new_user = User(
        email=student_data.email,
        hashed_password=hashed_password,
        is_student=True,
        is_active=True
    )
    db.add(new_user)
    db.flush()  # Get the user ID
    
    # Create student profile
    new_student = Student(
        user_id=new_user.id,
        full_name=student_data.full_name,
        mobile_number=student_data.mobile_number,
        student_id=student_data.student_id,
        course=student_data.course,
        year_of_study=student_data.year_of_study,
        college=student_data.college,
        first_login=True
    )
    db.add(new_student)
    db.commit()
    
    return {
        "message": "Student registered successfully",
        "email": student_data.email,
        "initial_password": "Your mobile number"
    }

@router.post("/student/login", response_model=Token)
async def login_student(
    login_data: StudentLoginRequest,
    db: Session = Depends(get_db)
):
    """Student login"""
    # Find user
    user = db.query(User).filter(
        User.email == login_data.email,
        User.is_student == True,
        User.is_active == True
    ).first()
    
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Get student profile
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "student_id": student.id,
            "role": "student",
            "first_login": student.first_login
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "student",
        "first_login": student.first_login,
        "profile_completed": student.profile_completed
    }

@router.post("/admin/login", response_model=Token)
async def login_admin(
    login_data: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """Admin login"""
    # Find user
    user = db.query(User).filter(
        User.email == login_data.email,
        User.is_admin == True,
        User.is_active == True
    ).first()
    
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Get admin profile
    admin = db.query(Admin).filter(Admin.user_id == user.id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin profile not found"
        )
    
    # Update last login
    admin.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "admin_id": admin.id,
            "role": "admin",
            "admin_role": admin.role
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "admin",
        "admin_role": admin.role
    }

@router.post("/student/change-password")
async def change_student_password(
    password_data: PasswordChangeRequest,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Change student password (especially for first login)"""
    if token_data.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can use this endpoint"
        )
    
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not user.verify_password(password_data.current_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    user.hashed_password = User.hash_password(password_data.new_password)
    
    # Update student first_login status
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if student and student.first_login:
        student.first_login = False
    
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/me")
async def get_current_user(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if token_data.get("role") == "student":
        student = db.query(Student).filter(Student.user_id == user.id).first()
        return {
            "user_type": "student",
            "email": user.email,
            "full_name": student.full_name if student else None,
            "mobile_number": student.mobile_number if student else None,
            "first_login": student.first_login if student else True,
            "profile_completed": student.profile_completed if student else False
        }
    elif token_data.get("role") == "admin":
        admin = db.query(Admin).filter(Admin.user_id == user.id).first()
        return {
            "user_type": "admin",
            "email": user.email,
            "full_name": admin.full_name if admin else None,
            "role": admin.role if admin else "admin",
            "department": admin.department if admin else None
        }
    
    return {"user_type": "unknown", "email": user.email}

