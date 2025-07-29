from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import time
import uuid
import logging

from app.db.session import get_db
from app.models.database import User, Candidate
from app.models.schemas import (
    Candidate as CandidateSchema, 
    CandidateCreate, 
    CandidateUpdate,
    ResumeAnalysisResult,
    APIResponse
)
from app.api.auth import get_current_active_user
from app.services.pdf_processor import PDFProcessor
from app.services.nlp_analyzer import NLPAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pdf_processor = PDFProcessor()
nlp_analyzer = NLPAnalyzer()

# File upload configuration
UPLOAD_DIR = "uploads/resumes"
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file."""
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    # Check file size (this is approximate, actual size check happens during upload)
    return True

def save_uploaded_file(file: UploadFile) -> str:
    """Save uploaded file and return the file path."""
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        if len(content) > MAX_FILE_SIZE:
            os.remove(file_path) if os.path.exists(file_path) else None
            raise HTTPException(status_code=413, detail="File too large")
        buffer.write(content)
    
    return file_path

def process_resume(file_path: str, candidate_data: dict) -> dict:
    """Process resume and extract information."""
    start_time = time.time()
    
    try:
        # Extract text from PDF
        resume_text, extraction_success = pdf_processor.extract_text_from_pdf(file_path)
        
        if not extraction_success:
            logger.warning(f"Limited text extraction from {file_path}")
        
        # Analyze document structure
        document_structure = pdf_processor.analyze_document_structure(resume_text)
        
        # Extract contact information
        contact_info = pdf_processor.extract_contact_information(resume_text)
        
        # Extract sections
        sections = pdf_processor.extract_sections(resume_text)
        
        # Perform NLP analysis
        extracted_skills = nlp_analyzer.extract_skills(resume_text)
        extracted_experience = nlp_analyzer.analyze_experience(resume_text)
        extracted_education = nlp_analyzer.analyze_education(resume_text)
        
        # Update contact info with extracted data if not provided
        if not candidate_data.get('name') and contact_info.get('name'):
            candidate_data['name'] = contact_info['name']
        if not candidate_data.get('email') and contact_info.get('email'):
            candidate_data['email'] = contact_info['email']
        if not candidate_data.get('phone') and contact_info.get('phone'):
            candidate_data['phone'] = contact_info['phone']
        
        processing_time = time.time() - start_time
        
        return {
            'analysis_success': extraction_success,
            'resume_text': resume_text,
            'extracted_skills': extracted_skills,
            'extracted_experience': extracted_experience,
            'extracted_education': extracted_education,
            'contact_information': contact_info,
            'document_structure': document_structure,
            'sections': sections,
            'processing_time_seconds': round(processing_time, 2)
        }
        
    except Exception as e:
        logger.error(f"Error processing resume {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Resume processing failed: {str(e)}")

@router.post("/upload", response_model=ResumeAnalysisResult)
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and process a resume."""
    
    # Validate file
    if not validate_file(file):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    try:
        # Save uploaded file
        file_path = save_uploaded_file(file)
        
        # Prepare candidate data
        candidate_data = {
            'name': name,
            'email': email,
            'phone': phone
        }
        
        # Process resume
        analysis_result = process_resume(file_path, candidate_data)
        
        # Create candidate record
        candidate = Candidate(
            name=candidate_data['name'],
            email=candidate_data['email'],
            phone=candidate_data.get('phone'),
            resume_filename=file.filename,
            resume_text=analysis_result['resume_text'],
            created_by_id=current_user.id
        )
        
        # Set extracted information
        candidate.set_extracted_skills(analysis_result['extracted_skills'])
        candidate.set_extracted_experience(analysis_result['extracted_experience'])
        candidate.set_extracted_education(analysis_result['extracted_education'])
        candidate.contact_information = str(analysis_result['contact_information'])
        
        # Save to database
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        # Return analysis result
        return ResumeAnalysisResult(
            candidate_id=candidate.id,
            analysis_success=analysis_result['analysis_success'],
            extracted_skills=analysis_result['extracted_skills'],
            extracted_experience=analysis_result['extracted_experience'],
            extracted_education=analysis_result['extracted_education'],
            contact_information=analysis_result['contact_information'],
            document_structure=analysis_result['document_structure'],
            processing_time_seconds=analysis_result['processing_time_seconds']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in resume upload: {str(e)}")
        # Clean up file if it was saved
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Resume upload failed")

@router.get("/candidates", response_model=List[CandidateSchema])
async def get_candidates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of candidates."""
    candidates = db.query(Candidate).filter(
        Candidate.created_by_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # Convert to schema format
    result = []
    for candidate in candidates:
        candidate_dict = {
            'id': candidate.id,
            'name': candidate.name,
            'email': candidate.email,
            'phone': candidate.phone,
            'resume_filename': candidate.resume_filename,
            'resume_text': candidate.resume_text,
            'extracted_skills': candidate.get_extracted_skills(),
            'extracted_experience': candidate.get_extracted_experience(),
            'extracted_education': candidate.get_extracted_education(),
            'contact_information': candidate.contact_information,
            'created_at': candidate.created_at,
            'updated_at': candidate.updated_at
        }
        result.append(candidate_dict)
    
    return result

@router.get("/candidates/{candidate_id}", response_model=CandidateSchema)
async def get_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get candidate by ID."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.created_by_id == current_user.id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return {
        'id': candidate.id,
        'name': candidate.name,
        'email': candidate.email,
        'phone': candidate.phone,
        'resume_filename': candidate.resume_filename,
        'resume_text': candidate.resume_text,
        'extracted_skills': candidate.get_extracted_skills(),
        'extracted_experience': candidate.get_extracted_experience(),
        'extracted_education': candidate.get_extracted_education(),
        'contact_information': candidate.contact_information,
        'created_at': candidate.created_at,
        'updated_at': candidate.updated_at
    }

@router.put("/candidates/{candidate_id}", response_model=CandidateSchema)
async def update_candidate(
    candidate_id: int,
    candidate_update: CandidateUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update candidate information."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.created_by_id == current_user.id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Update fields
    update_data = candidate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)
    
    db.commit()
    db.refresh(candidate)
    
    return {
        'id': candidate.id,
        'name': candidate.name,
        'email': candidate.email,
        'phone': candidate.phone,
        'resume_filename': candidate.resume_filename,
        'resume_text': candidate.resume_text,
        'extracted_skills': candidate.get_extracted_skills(),
        'extracted_experience': candidate.get_extracted_experience(),
        'extracted_education': candidate.get_extracted_education(),
        'contact_information': candidate.contact_information,
        'created_at': candidate.created_at,
        'updated_at': candidate.updated_at
    }

@router.delete("/candidates/{candidate_id}", response_model=APIResponse)
async def delete_candidate(
    candidate_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete candidate."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.created_by_id == current_user.id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    db.delete(candidate)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Candidate deleted successfully"
    )

@router.post("/candidates/{candidate_id}/reprocess", response_model=ResumeAnalysisResult)
async def reprocess_resume(
    candidate_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reprocess candidate's resume with updated algorithms."""
    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id,
        Candidate.created_by_id == current_user.id
    ).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    if not candidate.resume_text:
        raise HTTPException(status_code=400, detail="No resume text available for reprocessing")
    
    try:
        # Reprocess the existing resume text
        start_time = time.time()
        
        # Perform NLP analysis on existing text
        extracted_skills = nlp_analyzer.extract_skills(candidate.resume_text)
        extracted_experience = nlp_analyzer.analyze_experience(candidate.resume_text)
        extracted_education = nlp_analyzer.analyze_education(candidate.resume_text)
        
        # Update candidate record
        candidate.set_extracted_skills(extracted_skills)
        candidate.set_extracted_experience(extracted_experience)
        candidate.set_extracted_education(extracted_education)
        
        db.commit()
        db.refresh(candidate)
        
        processing_time = time.time() - start_time
        
        return ResumeAnalysisResult(
            candidate_id=candidate.id,
            analysis_success=True,
            extracted_skills=extracted_skills,
            extracted_experience=extracted_experience,
            extracted_education=extracted_education,
            contact_information=candidate.contact_information or {},
            document_structure={},
            processing_time_seconds=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error reprocessing resume for candidate {candidate_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Resume reprocessing failed")

