from src.models.user import db
from datetime import datetime
import json

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=False)
    resume_text = db.Column(db.Text, nullable=True)
    extracted_skills = db.Column(db.Text, nullable=True)  # JSON string
    extracted_experience = db.Column(db.Text, nullable=True)  # JSON string
    extracted_education = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'resume_filename': self.resume_filename,
            'resume_text': self.resume_text,
            'extracted_skills': json.loads(self.extracted_skills) if self.extracted_skills else [],
            'extracted_experience': json.loads(self.extracted_experience) if self.extracted_experience else [],
            'extracted_education': json.loads(self.extracted_education) if self.extracted_education else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, nullable=True)  # JSON string
    preferred_skills = db.Column(db.Text, nullable=True)  # JSON string
    experience_level = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    salary_range = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assessments = db.relationship('Assessment', backref='job_description', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'required_skills': json.loads(self.required_skills) if self.required_skills else [],
            'preferred_skills': json.loads(self.preferred_skills) if self.preferred_skills else [],
            'experience_level': self.experience_level,
            'location': self.location,
            'salary_range': self.salary_range,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)
    
    # Assessment scores (0-100)
    overall_score = db.Column(db.Float, nullable=True)
    technical_score = db.Column(db.Float, nullable=True)
    communication_score = db.Column(db.Float, nullable=True)
    cultural_fit_score = db.Column(db.Float, nullable=True)
    experience_match_score = db.Column(db.Float, nullable=True)
    
    # Assessment details
    strengths = db.Column(db.Text, nullable=True)  # JSON string
    weaknesses = db.Column(db.Text, nullable=True)  # JSON string
    recommendations = db.Column(db.Text, nullable=True)  # JSON string
    interview_questions = db.Column(db.Text, nullable=True)  # JSON string
    interview_responses = db.Column(db.Text, nullable=True)  # JSON string
    
    # Status and metadata
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed
    assessment_type = db.Column(db.String(50), default='comprehensive')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_description_id': self.job_description_id,
            'overall_score': self.overall_score,
            'technical_score': self.technical_score,
            'communication_score': self.communication_score,
            'cultural_fit_score': self.cultural_fit_score,
            'experience_match_score': self.experience_match_score,
            'strengths': json.loads(self.strengths) if self.strengths else [],
            'weaknesses': json.loads(self.weaknesses) if self.weaknesses else [],
            'recommendations': json.loads(self.recommendations) if self.recommendations else [],
            'interview_questions': json.loads(self.interview_questions) if self.interview_questions else [],
            'interview_responses': json.loads(self.interview_responses) if self.interview_responses else [],
            'status': self.status,
            'assessment_type': self.assessment_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

