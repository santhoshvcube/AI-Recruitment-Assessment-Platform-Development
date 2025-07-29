from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import uuid
import json
import logging
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.database import User, Candidate, JobDescription, Assessment, InterviewSession
from app.models.schemas import (
    InterviewQuestion,
    InterviewResponse,
    InterviewEvaluation,
    InterviewSessionCreate,
    InterviewSession as InterviewSessionSchema,
    AssessmentCreate,
    Assessment as AssessmentSchema,
    APIResponse
)
from app.api.auth import get_current_active_user
from app.services.interview_simulator import InterviewSimulator
from app.services.assessment_engine import AssessmentEngine

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
interview_simulator = InterviewSimulator()
assessment_engine = AssessmentEngine()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_token: str):
        await websocket.accept()
        self.active_connections[session_token] = websocket

    def disconnect(self, session_token: str):
        if session_token in self.active_connections:
            del self.active_connections[session_token]

    async def send_personal_message(self, message: dict, session_token: str):
        if session_token in self.active_connections:
            await self.active_connections[session_token].send_text(json.dumps(message))

manager = ConnectionManager()

@router.post("/start", response_model=InterviewSessionSchema)
async def start_interview_session(
    session_data: InterviewSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start a new interview session."""
    
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == session_data.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get candidate and job description
    candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
    job_description = db.query(JobDescription).filter(JobDescription.id == assessment.job_description_id).first()
    
    if not candidate or not job_description:
        raise HTTPException(status_code=404, detail="Candidate or job description not found")
    
    try:
        # Prepare candidate profile for question generation
        candidate_profile = {
            'id': candidate.id,
            'name': candidate.name,
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
        
        # Generate interview questions
        questions = interview_simulator.generate_interview_questions(
            candidate_profile, job_data, session_data.num_questions
        )
        
        # Create interview session
        session_token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=2)  # 2-hour session
        
        interview_session = InterviewSession(
            assessment_id=session_data.assessment_id,
            session_token=session_token,
            current_question_index=0,
            total_questions=len(questions),
            expires_at=expires_at
        )
        
        # Set questions data
        interview_session.set_questions_data(questions)
        interview_session.set_responses_data([])
        
        # Save to database
        db.add(interview_session)
        db.commit()
        db.refresh(interview_session)
        
        # Update assessment status
        assessment.status = "in_progress"
        assessment.set_interview_questions(questions)
        db.commit()
        
        return InterviewSessionSchema(
            id=interview_session.id,
            assessment_id=interview_session.assessment_id,
            session_token=interview_session.session_token,
            current_question_index=interview_session.current_question_index,
            total_questions=interview_session.total_questions,
            status=interview_session.status,
            started_at=interview_session.started_at,
            completed_at=interview_session.completed_at,
            expires_at=interview_session.expires_at
        )
        
    except Exception as e:
        logger.error(f"Error starting interview session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start interview session")

@router.get("/session/{session_token}", response_model=Dict)
async def get_interview_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Get interview session details."""
    
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    # Check if session is expired
    if datetime.utcnow() > session.expires_at:
        session.status = "expired"
        db.commit()
        raise HTTPException(status_code=410, detail="Interview session expired")
    
    questions = session.get_questions_data()
    responses = session.get_responses_data()
    
    # Get current question
    current_question = None
    if session.current_question_index < len(questions):
        current_question = questions[session.current_question_index]
    
    return {
        "session": {
            "id": session.id,
            "assessment_id": session.assessment_id,
            "session_token": session.session_token,
            "current_question_index": session.current_question_index,
            "total_questions": session.total_questions,
            "status": session.status,
            "started_at": session.started_at,
            "expires_at": session.expires_at
        },
        "current_question": current_question,
        "progress": {
            "completed": len(responses),
            "remaining": session.total_questions - len(responses),
            "percentage": (len(responses) / session.total_questions) * 100 if session.total_questions > 0 else 0
        }
    }

@router.post("/session/{session_token}/answer", response_model=Dict)
async def submit_answer(
    session_token: str,
    response: InterviewResponse,
    db: Session = Depends(get_db)
):
    """Submit an answer to the current interview question."""
    
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Interview session is not active")
    
    # Check if session is expired
    if datetime.utcnow() > session.expires_at:
        session.status = "expired"
        db.commit()
        raise HTTPException(status_code=410, detail="Interview session expired")
    
    try:
        questions = session.get_questions_data()
        responses = session.get_responses_data()
        
        # Validate question ID
        if response.question_id >= len(questions):
            raise HTTPException(status_code=400, detail="Invalid question ID")
        
        current_question = questions[response.question_id]
        
        # Get assessment and related data for evaluation
        assessment = db.query(Assessment).filter(Assessment.id == session.assessment_id).first()
        candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
        job_description = db.query(JobDescription).filter(JobDescription.id == assessment.job_description_id).first()
        
        # Prepare data for evaluation
        candidate_profile = {
            'extracted_skills': candidate.get_extracted_skills(),
            'extracted_experience': candidate.get_extracted_experience(),
            'extracted_education': candidate.get_extracted_education()
        }
        
        job_requirements = {
            'title': job_description.title,
            'required_skills': job_description.get_required_skills(),
            'preferred_skills': job_description.get_preferred_skills()
        }
        
        # Evaluate the response
        evaluation = interview_simulator.evaluate_response(
            current_question, response.response_text, candidate_profile, job_requirements
        )
        
        # Store response with evaluation
        response_data = {
            'question_id': response.question_id,
            'question': current_question,
            'response_text': response.response_text,
            'response_time_seconds': response.response_time_seconds,
            'evaluation': evaluation,
            'submitted_at': datetime.utcnow().isoformat()
        }
        
        responses.append(response_data)
        session.set_responses_data(responses)
        
        # Update current question index
        session.current_question_index = response.question_id + 1
        
        # Check if interview is complete
        if session.current_question_index >= session.total_questions:
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            
            # Update assessment with interview responses
            assessment.set_interview_responses(responses)
            assessment.status = "completed"
            assessment.completed_at = datetime.utcnow()
        
        db.commit()
        
        # Prepare next question
        next_question = None
        if session.current_question_index < len(questions):
            next_question = questions[session.current_question_index]
        
        return {
            "evaluation": evaluation,
            "next_question": next_question,
            "progress": {
                "completed": len(responses),
                "remaining": session.total_questions - len(responses),
                "percentage": (len(responses) / session.total_questions) * 100
            },
            "session_complete": session.status == "completed"
        }
        
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit answer")

@router.post("/session/{session_token}/pause", response_model=APIResponse)
async def pause_interview_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Pause an active interview session."""
    
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Can only pause active sessions")
    
    session.status = "paused"
    db.commit()
    
    return APIResponse(
        success=True,
        message="Interview session paused successfully"
    )

@router.post("/session/{session_token}/resume", response_model=APIResponse)
async def resume_interview_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Resume a paused interview session."""
    
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    if session.status != "paused":
        raise HTTPException(status_code=400, detail="Can only resume paused sessions")
    
    # Check if session is expired
    if datetime.utcnow() > session.expires_at:
        session.status = "expired"
        db.commit()
        raise HTTPException(status_code=410, detail="Interview session expired")
    
    session.status = "active"
    db.commit()
    
    return APIResponse(
        success=True,
        message="Interview session resumed successfully"
    )

@router.get("/session/{session_token}/results", response_model=Dict)
async def get_interview_results(
    session_token: str,
    db: Session = Depends(get_db)
):
    """Get interview results and evaluation summary."""
    
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")
    
    if session.status != "completed":
        raise HTTPException(status_code=400, detail="Interview session not completed")
    
    responses = session.get_responses_data()
    
    # Calculate summary statistics
    scores = []
    category_scores = {}
    
    for response in responses:
        evaluation = response.get('evaluation', {})
        overall_score = evaluation.get('overall_score', 0)
        scores.append(overall_score)
        
        question = response.get('question', {})
        category = question.get('category', 'unknown')
        
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(overall_score)
    
    # Calculate averages
    overall_average = sum(scores) / len(scores) if scores else 0
    category_averages = {
        category: sum(scores) / len(scores)
        for category, scores in category_scores.items()
    }
    
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == session.assessment_id).first()
    
    return {
        "session_summary": {
            "total_questions": session.total_questions,
            "completed_questions": len(responses),
            "overall_score": round(overall_average, 2),
            "category_scores": category_averages,
            "duration_minutes": (session.completed_at - session.started_at).total_seconds() / 60 if session.completed_at else 0
        },
        "detailed_responses": responses,
        "assessment_id": assessment.id if assessment else None
    }

@router.websocket("/ws/{session_token}")
async def websocket_endpoint(websocket: WebSocket, session_token: str, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time interview communication."""
    
    # Validate session
    session = db.query(InterviewSession).filter(
        InterviewSession.session_token == session_token
    ).first()
    
    if not session:
        await websocket.close(code=4004, reason="Session not found")
        return
    
    await manager.connect(websocket, session_token)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_personal_message({"type": "pong"}, session_token)
            
            elif message.get("type") == "get_current_question":
                questions = session.get_questions_data()
                if session.current_question_index < len(questions):
                    current_question = questions[session.current_question_index]
                    await manager.send_personal_message({
                        "type": "current_question",
                        "question": current_question
                    }, session_token)
            
            elif message.get("type") == "session_status":
                await manager.send_personal_message({
                    "type": "session_status",
                    "status": session.status,
                    "current_question_index": session.current_question_index,
                    "total_questions": session.total_questions
                }, session_token)
            
    except WebSocketDisconnect:
        manager.disconnect(session_token)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(session_token)

