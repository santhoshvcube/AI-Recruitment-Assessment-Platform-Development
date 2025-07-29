from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from passlib.context import CryptContext
import re

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """Base user model with common fields"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_student = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, self.hashed_password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

class Student(Base):
    """Student-specific model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)  # Foreign key to User
    full_name = Column(String(255), nullable=False)
    mobile_number = Column(String(20), nullable=False, unique=True)
    student_id = Column(String(50), nullable=True, unique=True)
    course = Column(String(255), nullable=True)
    year_of_study = Column(String(10), nullable=True)
    college = Column(String(255), nullable=True)
    first_login = Column(Boolean, default=True)
    profile_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    @staticmethod
    def validate_mobile_number(mobile: str) -> bool:
        """Validate mobile number format"""
        # Basic validation for mobile number (10 digits)
        pattern = r'^[6-9]\d{9}$'
        return bool(re.match(pattern, mobile))

class Admin(Base):
    """Admin-specific model"""
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)  # Foreign key to User
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")  # admin, super_admin, hr_manager
    department = Column(String(255), nullable=True)
    permissions = Column(Text, nullable=True)  # JSON string of permissions
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assessment(Base):
    """Assessment model linking students to their assessments"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)  # Foreign key to Student
    admin_id = Column(Integer, nullable=False)  # Foreign key to Admin (who created)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)
    resume_filename = Column(String(255), nullable=True)
    resume_path = Column(String(500), nullable=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    overall_score = Column(Integer, nullable=True)
    recommendation = Column(String(50), nullable=True)  # strong_hire, hire, maybe, no_hire
    assessment_data = Column(Text, nullable=True)  # JSON string of detailed assessment
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class Interview(Base):
    """Interview session model"""
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, nullable=False)  # Foreign key to Assessment
    student_id = Column(Integer, nullable=False)  # Foreign key to Student
    status = Column(String(50), default="scheduled")  # scheduled, in_progress, completed
    questions = Column(Text, nullable=True)  # JSON string of questions
    responses = Column(Text, nullable=True)  # JSON string of responses
    duration_minutes = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class FreeTrialUser(Base):
    """Free Trial User model"""
    __tablename__ = "free_trial_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    trial_start_time = Column(DateTime(timezone=True), server_default=func.now())
    trial_end_time = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)


