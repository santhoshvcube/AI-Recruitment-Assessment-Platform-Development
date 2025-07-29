from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Dict, Optional
import os
import uuid
import json
import logging
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.database import User, Assessment, Candidate, JobDescription
from app.models.schemas import (
    ReportRequest,
    ReportResponse,
    APIResponse
)
from app.api.auth import get_current_active_user
from app.services.assessment_engine import AssessmentEngine
from app.services.report_generator import ReportGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
assessment_engine = AssessmentEngine()
report_generator = ReportGenerator()

# Report storage configuration
REPORTS_DIR = "generated_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.post("/generate", response_model=ReportResponse)
async def generate_assessment_report(
    report_request: ReportRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a comprehensive assessment report."""
    
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == report_request.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get related data
    candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
    job_description = db.query(JobDescription).filter(JobDescription.id == assessment.job_description_id).first()
    
    if not candidate or not job_description:
        raise HTTPException(status_code=404, detail="Related data not found")
    
    try:
        # If assessment is not completed, run comprehensive assessment
        if assessment.status != "completed" or not assessment.overall_score:
            # Prepare candidate data
            candidate_data = {
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'resume_text': candidate.resume_text,
                'extracted_skills': candidate.get_extracted_skills(),
                'extracted_experience': candidate.get_extracted_experience(),
                'extracted_education': candidate.get_extracted_education()
            }
            
            # Prepare job description data
            job_data = {
                'id': job_description.id,
                'title': job_description.title,
                'company': job_description.company,
                'description': job_description.description,
                'required_skills': job_description.get_required_skills(),
                'preferred_skills': job_description.get_preferred_skills(),
                'experience_level': job_description.experience_level
            }
            
            # Get interview responses if available
            interview_responses = assessment.get_interview_responses()
            
            # Run comprehensive assessment
            assessment_result = assessment_engine.conduct_comprehensive_assessment(
                candidate_data, job_data, interview_responses
            )
            
            # Update assessment with results
            assessment.overall_score = assessment_result['overall_score']
            assessment.confidence_level = assessment_result['confidence_level']
            assessment.hiring_recommendation = assessment_result['hiring_recommendation']
            
            # Update component scores
            component_scores = assessment_result['component_scores']
            assessment.resume_analysis_score = component_scores.get('resume_analysis', {}).get('overall_score')
            assessment.skill_match_score = component_scores.get('skill_match', {}).get('overall_score')
            assessment.experience_relevance_score = component_scores.get('experience_relevance', {}).get('overall_score')
            assessment.interview_performance_score = component_scores.get('interview_performance', {}).get('overall_score')
            assessment.cultural_fit_score = component_scores.get('cultural_fit', {}).get('overall_score')
            
            # Update detailed analysis
            assessment.set_detailed_analysis(assessment_result['detailed_analysis'])
            assessment.set_strengths(assessment_result['strengths'])
            assessment.set_development_areas(assessment_result['development_areas'])
            assessment.set_risk_factors(assessment_result['risk_factors'])
            assessment.set_recommendations(assessment_result['recommendations'])
            
            assessment.status = "completed"
            assessment.completed_at = datetime.utcnow()
            
            db.commit()
            db.refresh(assessment)
        
        # Prepare report data
        report_data = {
            'assessment': {
                'id': assessment.id,
                'overall_score': assessment.overall_score,
                'confidence_level': assessment.confidence_level,
                'hiring_recommendation': assessment.hiring_recommendation,
                'status': assessment.status,
                'created_at': assessment.created_at,
                'completed_at': assessment.completed_at,
                'component_scores': {
                    'resume_analysis': assessment.resume_analysis_score,
                    'skill_match': assessment.skill_match_score,
                    'experience_relevance': assessment.experience_relevance_score,
                    'interview_performance': assessment.interview_performance_score,
                    'cultural_fit': assessment.cultural_fit_score
                },
                'detailed_analysis': assessment.get_detailed_analysis(),
                'strengths': assessment.get_strengths(),
                'development_areas': assessment.get_development_areas(),
                'risk_factors': assessment.get_risk_factors(),
                'recommendations': assessment.get_recommendations()
            },
            'candidate': {
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'extracted_skills': candidate.get_extracted_skills(),
                'extracted_experience': candidate.get_extracted_experience(),
                'extracted_education': candidate.get_extracted_education()
            },
            'job_description': {
                'id': job_description.id,
                'title': job_description.title,
                'company': job_description.company,
                'description': job_description.description,
                'required_skills': job_description.get_required_skills(),
                'preferred_skills': job_description.get_preferred_skills(),
                'experience_level': job_description.experience_level,
                'location': job_description.location
            },
            'interview_responses': assessment.get_interview_responses() if report_request.include_interview_responses else [],
            'metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'generated_by': current_user.username,
                'format': report_request.format,
                'include_detailed_analysis': report_request.include_detailed_analysis,
                'include_interview_responses': report_request.include_interview_responses
            }
        }
        
        # Generate report file
        report_id = str(uuid.uuid4())
        
        if report_request.format == "pdf":
            file_path = await report_generator.generate_pdf_report(report_data, report_id, REPORTS_DIR)
        elif report_request.format == "html":
            file_path = await report_generator.generate_html_report(report_data, report_id, REPORTS_DIR)
        elif report_request.format == "json":
            file_path = await report_generator.generate_json_report(report_data, report_id, REPORTS_DIR)
        else:
            raise HTTPException(status_code=400, detail="Unsupported report format")
        
        # Set expiration (reports expire after 7 days)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        return ReportResponse(
            report_id=report_id,
            assessment_id=assessment.id,
            format=report_request.format,
            file_path=file_path,
            download_url=f"/api/report/download/{report_id}",
            generated_at=datetime.utcnow(),
            expires_at=expires_at
        )
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Report generation failed")

@router.get("/download/{report_id}")
async def download_report(
    report_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Download a generated report."""
    
    # Find report file
    possible_extensions = ['.pdf', '.html', '.json']
    file_path = None
    
    for ext in possible_extensions:
        potential_path = os.path.join(REPORTS_DIR, f"{report_id}{ext}")
        if os.path.exists(potential_path):
            file_path = potential_path
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Determine media type
    if file_path.endswith('.pdf'):
        media_type = 'application/pdf'
        filename = f"assessment_report_{report_id}.pdf"
    elif file_path.endswith('.html'):
        media_type = 'text/html'
        filename = f"assessment_report_{report_id}.html"
    elif file_path.endswith('.json'):
        media_type = 'application/json'
        filename = f"assessment_report_{report_id}.json"
    else:
        media_type = 'application/octet-stream'
        filename = f"assessment_report_{report_id}"
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )

@router.get("/assessment/{assessment_id}/summary", response_model=Dict)
async def get_assessment_summary(
    assessment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get assessment summary without generating full report."""
    
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
    job_description = db.query(JobDescription).filter(JobDescription.id == assessment.job_description_id).first()
    
    return {
        'assessment_id': assessment.id,
        'candidate_name': candidate.name if candidate else 'Unknown',
        'job_title': job_description.title if job_description else 'Unknown',
        'overall_score': assessment.overall_score,
        'confidence_level': assessment.confidence_level,
        'hiring_recommendation': assessment.hiring_recommendation,
        'status': assessment.status,
        'component_scores': {
            'resume_analysis': assessment.resume_analysis_score,
            'skill_match': assessment.skill_match_score,
            'experience_relevance': assessment.experience_relevance_score,
            'interview_performance': assessment.interview_performance_score,
            'cultural_fit': assessment.cultural_fit_score
        },
        'strengths': assessment.get_strengths()[:3],  # Top 3 strengths
        'development_areas': assessment.get_development_areas()[:3],  # Top 3 areas
        'created_at': assessment.created_at,
        'completed_at': assessment.completed_at
    }

@router.get("/assessment/{assessment_id}/detailed", response_model=Dict)
async def get_detailed_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed assessment data."""
    
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
    job_description = db.query(JobDescription).filter(JobDescription.id == assessment.job_description_id).first()
    
    return {
        'assessment': {
            'id': assessment.id,
            'overall_score': assessment.overall_score,
            'confidence_level': assessment.confidence_level,
            'hiring_recommendation': assessment.hiring_recommendation,
            'status': assessment.status,
            'component_scores': {
                'resume_analysis': assessment.resume_analysis_score,
                'skill_match': assessment.skill_match_score,
                'experience_relevance': assessment.experience_relevance_score,
                'interview_performance': assessment.interview_performance_score,
                'cultural_fit': assessment.cultural_fit_score
            },
            'detailed_analysis': assessment.get_detailed_analysis(),
            'strengths': assessment.get_strengths(),
            'development_areas': assessment.get_development_areas(),
            'risk_factors': assessment.get_risk_factors(),
            'recommendations': assessment.get_recommendations(),
            'created_at': assessment.created_at,
            'completed_at': assessment.completed_at
        },
        'candidate': {
            'id': candidate.id,
            'name': candidate.name,
            'email': candidate.email,
            'extracted_skills': candidate.get_extracted_skills(),
            'extracted_experience': candidate.get_extracted_experience(),
            'extracted_education': candidate.get_extracted_education()
        },
        'job_description': {
            'id': job_description.id,
            'title': job_description.title,
            'company': job_description.company,
            'required_skills': job_description.get_required_skills(),
            'preferred_skills': job_description.get_preferred_skills(),
            'experience_level': job_description.experience_level
        },
        'interview_data': {
            'questions': assessment.get_interview_questions(),
            'responses': assessment.get_interview_responses()
        }
    }

@router.delete("/cleanup", response_model=APIResponse)
async def cleanup_expired_reports(
    current_user: User = Depends(get_current_active_user)
):
    """Clean up expired report files (admin only)."""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        cleaned_count = 0
        
        # Get all files in reports directory
        if os.path.exists(REPORTS_DIR):
            for filename in os.listdir(REPORTS_DIR):
                file_path = os.path.join(REPORTS_DIR, filename)
                
                # Check file age (remove files older than 7 days)
                file_age = datetime.utcnow() - datetime.fromtimestamp(os.path.getctime(file_path))
                if file_age > timedelta(days=7):
                    os.remove(file_path)
                    cleaned_count += 1
        
        return APIResponse(
            success=True,
            message=f"Cleaned up {cleaned_count} expired report files"
        )
        
    except Exception as e:
        logger.error(f"Error cleaning up reports: {str(e)}")
        raise HTTPException(status_code=500, detail="Cleanup failed")

@router.get("/formats", response_model=Dict)
async def get_supported_formats():
    """Get list of supported report formats."""
    
    return {
        "supported_formats": [
            {
                "format": "pdf",
                "description": "Portable Document Format - Professional report suitable for sharing",
                "mime_type": "application/pdf"
            },
            {
                "format": "html",
                "description": "HTML format - Interactive report viewable in web browsers",
                "mime_type": "text/html"
            },
            {
                "format": "json",
                "description": "JSON format - Structured data for API integration",
                "mime_type": "application/json"
            }
        ],
        "default_format": "pdf"
    }

