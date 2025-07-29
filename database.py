from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="recruiter")  # recruiter, admin, candidate
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidates = relationship("Candidate", back_populates="created_by")
    job_descriptions = relationship("JobDescription", back_populates="created_by")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    resume_filename = Column(String(255), nullable=False)
    resume_text = Column(Text, nullable=True)
    
    # Extracted information (stored as JSON strings)
    extracted_skills = Column(Text, nullable=True)
    extracted_experience = Column(Text, nullable=True)
    extracted_education = Column(Text, nullable=True)
    contact_information = Column(Text, nullable=True)
    
    # Metadata
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    created_by = relationship("User", back_populates="candidates")
    assessments = relationship("Assessment", back_populates="candidate", cascade="all, delete-orphan")
    
    def get_extracted_skills(self):
        return json.loads(self.extracted_skills) if self.extracted_skills else {}
    
    def set_extracted_skills(self, skills_dict):
        self.extracted_skills = json.dumps(skills_dict)
    
    def get_extracted_experience(self):
        return json.loads(self.extracted_experience) if self.extracted_experience else {}
    
    def set_extracted_experience(self, experience_dict):
        self.extracted_experience = json.dumps(experience_dict)
    
    def get_extracted_education(self):
        return json.loads(self.extracted_education) if self.extracted_education else {}
    
    def set_extracted_education(self, education_dict):
        self.extracted_education = json.dumps(education_dict)

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    
    # Requirements (stored as JSON strings)
    required_skills = Column(Text, nullable=True)
    preferred_skills = Column(Text, nullable=True)
    
    # Job details
    experience_level = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    salary_range = Column(String(50), nullable=True)
    employment_type = Column(String(50), default="full_time")
    
    # Metadata
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    created_by = relationship("User", back_populates="job_descriptions")
    assessments = relationship("Assessment", back_populates="job_description")
    
    def get_required_skills(self):
        return json.loads(self.required_skills) if self.required_skills else []
    
    def set_required_skills(self, skills_list):
        self.required_skills = json.dumps(skills_list)
    
    def get_preferred_skills(self):
        return json.loads(self.preferred_skills) if self.preferred_skills else []
    
    def set_preferred_skills(self, skills_list):
        self.preferred_skills = json.dumps(skills_list)

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    
    # Overall assessment scores (0-100)
    overall_score = Column(Float, nullable=True)
    confidence_level = Column(Float, nullable=True)
    
    # Component scores (0-100)
    resume_analysis_score = Column(Float, nullable=True)
    skill_match_score = Column(Float, nullable=True)
    experience_relevance_score = Column(Float, nullable=True)
    interview_performance_score = Column(Float, nullable=True)
    cultural_fit_score = Column(Float, nullable=True)
    
    # Assessment details (stored as JSON strings)
    detailed_analysis = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    development_areas = Column(Text, nullable=True)
    risk_factors = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    
    # Interview data
    interview_questions = Column(Text, nullable=True)
    interview_responses = Column(Text, nullable=True)
    
    # Status and metadata
    status = Column(String(50), default="pending")  # pending, in_progress, completed, archived
    assessment_type = Column(String(50), default="comprehensive")
    hiring_recommendation = Column(String(50), nullable=True)  # strong_hire, hire, maybe, no_hire
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="assessments")
    job_description = relationship("JobDescription", back_populates="assessments")
    
    def get_detailed_analysis(self):
        return json.loads(self.detailed_analysis) if self.detailed_analysis else {}
    
    def set_detailed_analysis(self, analysis_dict):
        self.detailed_analysis = json.dumps(analysis_dict)
    
    def get_strengths(self):
        return json.loads(self.strengths) if self.strengths else []
    
    def set_strengths(self, strengths_list):
        self.strengths = json.dumps(strengths_list)
    
    def get_development_areas(self):
        return json.loads(self.development_areas) if self.development_areas else []
    
    def set_development_areas(self, areas_list):
        self.development_areas = json.dumps(areas_list)
    
    def get_risk_factors(self):
        return json.loads(self.risk_factors) if self.risk_factors else []
    
    def set_risk_factors(self, risks_list):
        self.risk_factors = json.dumps(risks_list)
    
    def get_recommendations(self):
        return json.loads(self.recommendations) if self.recommendations else {}
    
    def set_recommendations(self, recommendations_dict):
        self.recommendations = json.dumps(recommendations_dict)
    
    def get_interview_questions(self):
        return json.loads(self.interview_questions) if self.interview_questions else []
    
    def set_interview_questions(self, questions_list):
        self.interview_questions = json.dumps(questions_list)
    
    def get_interview_responses(self):
        return json.loads(self.interview_responses) if self.interview_responses else []
    
    def set_interview_responses(self, responses_list):
        self.interview_responses = json.dumps(responses_list)

class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    
    # Session details
    session_token = Column(String(255), unique=True, index=True, nullable=False)
    current_question_index = Column(Integer, default=0)
    total_questions = Column(Integer, nullable=False)
    
    # Session status
    status = Column(String(50), default="active")  # active, paused, completed, expired
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Session data
    questions_data = Column(Text, nullable=True)  # JSON string of questions
    responses_data = Column(Text, nullable=True)  # JSON string of responses
    session_metadata = Column(Text, nullable=True)  # Additional session info
    
    def get_questions_data(self):
        return json.loads(self.questions_data) if self.questions_data else []
    
    def set_questions_data(self, questions_list):
        self.questions_data = json.dumps(questions_list)
    
    def get_responses_data(self):
        return json.loads(self.responses_data) if self.responses_data else []
    
    def set_responses_data(self, responses_list):
        self.responses_data = json.dumps(responses_list)
    
    def get_session_metadata(self):
        return json.loads(self.session_metadata) if self.session_metadata else {}
    
    def set_session_metadata(self, metadata_dict):
        self.session_metadata = json.dumps(metadata_dict)

