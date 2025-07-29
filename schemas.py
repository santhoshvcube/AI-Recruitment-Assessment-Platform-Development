from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    recruiter = "recruiter"
    admin = "admin"
    candidate = "candidate"

class AssessmentStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    archived = "archived"

class HiringRecommendation(str, Enum):
    strong_hire = "strong_hire"
    hire = "hire"
    maybe = "maybe"
    no_hire = "no_hire"
    manual_review = "manual_review"

class InterviewSessionStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    expired = "expired"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    role: UserRole = UserRole.recruiter

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Candidate schemas
class CandidateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class Candidate(CandidateBase):
    id: int
    resume_filename: str
    resume_text: Optional[str] = None
    extracted_skills: Optional[Dict[str, Any]] = None
    extracted_experience: Optional[Dict[str, Any]] = None
    extracted_education: Optional[Dict[str, Any]] = None
    contact_information: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Job Description schemas
class JobDescriptionBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    company: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    experience_level: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    employment_type: str = "full_time"

class JobDescriptionCreate(JobDescriptionBase):
    required_skills: Optional[List[str]] = []
    preferred_skills: Optional[List[str]] = []

class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None
    is_active: Optional[bool] = None

class JobDescription(JobDescriptionBase):
    id: int
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Assessment schemas
class AssessmentBase(BaseModel):
    candidate_id: int
    job_description_id: int
    assessment_type: str = "comprehensive"

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentUpdate(BaseModel):
    status: Optional[AssessmentStatus] = None
    overall_score: Optional[float] = None
    confidence_level: Optional[float] = None
    hiring_recommendation: Optional[HiringRecommendation] = None

class Assessment(AssessmentBase):
    id: int
    overall_score: Optional[float] = None
    confidence_level: Optional[float] = None
    resume_analysis_score: Optional[float] = None
    skill_match_score: Optional[float] = None
    experience_relevance_score: Optional[float] = None
    interview_performance_score: Optional[float] = None
    cultural_fit_score: Optional[float] = None
    detailed_analysis: Optional[Dict[str, Any]] = None
    strengths: Optional[List[str]] = None
    development_areas: Optional[List[str]] = None
    risk_factors: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[Dict[str, Any]] = None
    status: AssessmentStatus
    hiring_recommendation: Optional[HiringRecommendation] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Interview schemas
class InterviewQuestion(BaseModel):
    question: str
    category: str
    type: str
    difficulty: str = "medium"
    estimated_time_minutes: int = 5
    follow_up: Optional[str] = None
    question_number: Optional[int] = None

class InterviewResponse(BaseModel):
    question_id: int
    response_text: str
    response_time_seconds: Optional[int] = None

class InterviewEvaluation(BaseModel):
    question_id: int
    overall_score: float
    scores: Dict[str, float]
    strengths: List[str]
    areas_for_improvement: List[str]
    feedback: str
    recommendation: str

class InterviewSessionCreate(BaseModel):
    assessment_id: int
    num_questions: int = 10

class InterviewSession(BaseModel):
    id: int
    assessment_id: int
    session_token: str
    current_question_index: int
    total_questions: int
    status: InterviewSessionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: datetime
    
    class Config:
        from_attributes = True

# Resume upload schemas
class ResumeUpload(BaseModel):
    candidate_data: CandidateCreate

class ResumeAnalysisResult(BaseModel):
    candidate_id: int
    analysis_success: bool
    extracted_skills: Dict[str, Any]
    extracted_experience: Dict[str, Any]
    extracted_education: Dict[str, Any]
    contact_information: Dict[str, Any]
    document_structure: Dict[str, Any]
    processing_time_seconds: float

# Report schemas
class ReportRequest(BaseModel):
    assessment_id: int
    format: str = "pdf"  # pdf, html, json
    include_detailed_analysis: bool = True
    include_interview_responses: bool = True

class ReportResponse(BaseModel):
    report_id: str
    assessment_id: int
    format: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None
    generated_at: datetime
    expires_at: Optional[datetime] = None

# API Response schemas
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int

# Health check schema
class HealthCheck(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime



class FreeTrialUserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=8)

class FreeTrialUserLogin(BaseModel):
    email: EmailStr
    password: str



