import openai
import json
import re
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class InterviewSimulator:
    """
    AI-powered interview simulation service.
    Generates contextual questions and evaluates candidate responses.
    """
    
    def __init__(self):
        self.client = openai.OpenAI()
        
        # Question categories and types
        self.question_categories = {
            'technical': {
                'weight': 0.4,
                'subcategories': ['coding', 'system_design', 'problem_solving', 'tools_technologies']
            },
            'behavioral': {
                'weight': 0.3,
                'subcategories': ['leadership', 'teamwork', 'conflict_resolution', 'adaptability']
            },
            'situational': {
                'weight': 0.2,
                'subcategories': ['decision_making', 'prioritization', 'crisis_management']
            },
            'cultural_fit': {
                'weight': 0.1,
                'subcategories': ['values_alignment', 'work_style', 'motivation']
            }
        }
        
        # Evaluation criteria
        self.evaluation_criteria = {
            'technical_accuracy': {
                'weight': 0.25,
                'description': 'Correctness and depth of technical knowledge'
            },
            'communication_clarity': {
                'weight': 0.20,
                'description': 'Ability to explain concepts clearly and concisely'
            },
            'problem_solving_approach': {
                'weight': 0.20,
                'description': 'Systematic approach to solving problems'
            },
            'experience_relevance': {
                'weight': 0.15,
                'description': 'Relevance of past experience to the role'
            },
            'cultural_alignment': {
                'weight': 0.10,
                'description': 'Alignment with company culture and values'
            },
            'growth_potential': {
                'weight': 0.10,
                'description': 'Potential for learning and career growth'
            }
        }
    
    def generate_interview_questions(self, 
                                   candidate_profile: Dict, 
                                   job_description: Dict,
                                   num_questions: int = 10) -> List[Dict]:
        """
        Generate personalized interview questions based on candidate profile and job requirements.
        
        Args:
            candidate_profile: Candidate information including skills and experience
            job_description: Job requirements and description
            num_questions: Number of questions to generate
            
        Returns:
            List of interview questions with metadata
        """
        try:
            # Distribute questions across categories
            question_distribution = self._calculate_question_distribution(num_questions)
            
            questions = []
            
            for category, count in question_distribution.items():
                if count > 0:
                    category_questions = self._generate_category_questions(
                        category, count, candidate_profile, job_description
                    )
                    questions.extend(category_questions)
            
            # Shuffle and add metadata
            import random
            random.shuffle(questions)
            
            # Add question numbers and timing
            for i, question in enumerate(questions):
                question['question_number'] = i + 1
                question['estimated_time_minutes'] = self._estimate_question_time(question)
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating interview questions: {str(e)}")
            return self._get_fallback_questions(num_questions)
    
    def _calculate_question_distribution(self, total_questions: int) -> Dict[str, int]:
        """
        Calculate how many questions to generate for each category.
        """
        distribution = {}
        remaining_questions = total_questions
        
        for category, config in self.question_categories.items():
            count = max(1, int(total_questions * config['weight']))
            distribution[category] = min(count, remaining_questions)
            remaining_questions -= distribution[category]
            
            if remaining_questions <= 0:
                break
        
        # Distribute any remaining questions
        categories = list(distribution.keys())
        i = 0
        while remaining_questions > 0 and categories:
            distribution[categories[i]] += 1
            remaining_questions -= 1
            i = (i + 1) % len(categories)
        
        return distribution
    
    def _generate_category_questions(self, 
                                   category: str, 
                                   count: int,
                                   candidate_profile: Dict,
                                   job_description: Dict) -> List[Dict]:
        """
        Generate questions for a specific category.
        """
        try:
            prompt = self._build_question_generation_prompt(
                category, count, candidate_profile, job_description
            )
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical recruiter and interview specialist. Generate thoughtful, relevant interview questions that assess candidate suitability for the role."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            questions_text = response.choices[0].message.content
            questions = self._parse_generated_questions(questions_text, category)
            
            return questions[:count]  # Ensure we don't exceed requested count
            
        except Exception as e:
            logger.error(f"Error generating {category} questions: {str(e)}")
            return self._get_fallback_category_questions(category, count)
    
    def _build_question_generation_prompt(self, 
                                        category: str,
                                        count: int,
                                        candidate_profile: Dict,
                                        job_description: Dict) -> str:
        """
        Build prompt for question generation.
        """
        candidate_skills = candidate_profile.get('extracted_skills', {}).get('all_skills', [])
        candidate_experience = candidate_profile.get('extracted_experience', {})
        
        job_title = job_description.get('title', 'Software Engineer')
        job_requirements = job_description.get('required_skills', [])
        job_desc_text = job_description.get('description', '')
        
        prompt = f"""
Generate {count} {category} interview questions for a {job_title} position.

CANDIDATE PROFILE:
- Skills: {', '.join(candidate_skills[:10])}
- Experience Level: {candidate_experience.get('experience_level', 'mid')}
- Total Years: {candidate_experience.get('total_years', 'Unknown')}
- Previous Roles: {', '.join(candidate_experience.get('job_titles', [])[:3])}

JOB REQUIREMENTS:
- Position: {job_title}
- Required Skills: {', '.join(job_requirements[:10])}
- Job Description: {job_desc_text[:500]}...

QUESTION CATEGORY: {category.upper()}

Requirements:
1. Questions should be specific to the candidate's background and job requirements
2. Include a mix of difficulty levels appropriate for the candidate's experience
3. Focus on practical, real-world scenarios
4. Ensure questions can be answered in 3-5 minutes each
5. Include follow-up question suggestions where appropriate

Format each question as:
Q: [Question text]
Type: [specific_type]
Difficulty: [easy/medium/hard]
Follow-up: [optional follow-up question]
---
"""
        
        return prompt
    
    def _parse_generated_questions(self, questions_text: str, category: str) -> List[Dict]:
        """
        Parse generated questions from AI response.
        """
        questions = []
        question_blocks = questions_text.split('---')
        
        for block in question_blocks:
            if not block.strip():
                continue
                
            question_data = {
                'category': category,
                'question': '',
                'type': category,
                'difficulty': 'medium',
                'follow_up': None,
                'expected_duration_minutes': 5
            }
            
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Q:'):
                    question_data['question'] = line[2:].strip()
                elif line.startswith('Type:'):
                    question_data['type'] = line[5:].strip()
                elif line.startswith('Difficulty:'):
                    question_data['difficulty'] = line[11:].strip().lower()
                elif line.startswith('Follow-up:'):
                    follow_up = line[10:].strip()
                    if follow_up and follow_up != 'None':
                        question_data['follow_up'] = follow_up
            
            if question_data['question']:
                questions.append(question_data)
        
        return questions
    
    def _estimate_question_time(self, question: Dict) -> int:
        """
        Estimate time needed to answer a question.
        """
        base_time = 3  # Base 3 minutes
        
        # Adjust based on difficulty
        difficulty_multiplier = {
            'easy': 0.8,
            'medium': 1.0,
            'hard': 1.5
        }
        
        multiplier = difficulty_multiplier.get(question.get('difficulty', 'medium'), 1.0)
        
        # Adjust based on category
        category_time = {
            'technical': 5,
            'behavioral': 4,
            'situational': 4,
            'cultural_fit': 3
        }
        
        base_time = category_time.get(question.get('category', 'technical'), 4)
        
        return int(base_time * multiplier)
    
    def evaluate_response(self, 
                         question: Dict, 
                         response: str,
                         candidate_profile: Dict,
                         job_requirements: Dict) -> Dict:
        """
        Evaluate candidate response to an interview question.
        
        Args:
            question: Interview question data
            response: Candidate's response
            candidate_profile: Candidate information
            job_requirements: Job requirements
            
        Returns:
            Evaluation results with scores and feedback
        """
        try:
            evaluation_prompt = self._build_evaluation_prompt(
                question, response, candidate_profile, job_requirements
            )
            
            response_obj = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interview evaluator. Provide objective, constructive assessment of candidate responses with specific scores and actionable feedback."
                    },
                    {
                        "role": "user",
                        "content": evaluation_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            evaluation_text = response_obj.choices[0].message.content
            evaluation = self._parse_evaluation_response(evaluation_text)
            
            # Add metadata
            evaluation['question_id'] = question.get('question_number', 0)
            evaluation['question_category'] = question.get('category', 'unknown')
            evaluation['response_length'] = len(response.split())
            evaluation['evaluated_at'] = datetime.utcnow().isoformat()
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            return self._get_fallback_evaluation()
    
    def _build_evaluation_prompt(self, 
                               question: Dict,
                               response: str,
                               candidate_profile: Dict,
                               job_requirements: Dict) -> str:
        """
        Build prompt for response evaluation.
        """
        prompt = f"""
Evaluate this interview response objectively and provide detailed feedback.

QUESTION:
Category: {question.get('category', 'unknown')}
Type: {question.get('type', 'unknown')}
Difficulty: {question.get('difficulty', 'medium')}
Question: {question.get('question', '')}

CANDIDATE RESPONSE:
{response}

CANDIDATE CONTEXT:
- Experience Level: {candidate_profile.get('extracted_experience', {}).get('experience_level', 'unknown')}
- Total Years: {candidate_profile.get('extracted_experience', {}).get('total_years', 'unknown')}
- Relevant Skills: {', '.join(candidate_profile.get('extracted_skills', {}).get('all_skills', [])[:10])}

JOB CONTEXT:
- Position: {job_requirements.get('title', 'Unknown')}
- Required Skills: {', '.join(job_requirements.get('required_skills', [])[:10])}

EVALUATION CRITERIA:
1. Technical Accuracy (0-100): Correctness and depth of technical knowledge
2. Communication Clarity (0-100): Ability to explain concepts clearly
3. Problem Solving Approach (0-100): Systematic approach to problem solving
4. Experience Relevance (0-100): Relevance of examples and experience
5. Cultural Alignment (0-100): Fit with role and company culture
6. Growth Potential (0-100): Demonstrated learning ability and potential

Provide evaluation in this format:
SCORES:
Technical Accuracy: [score]/100
Communication Clarity: [score]/100
Problem Solving Approach: [score]/100
Experience Relevance: [score]/100
Cultural Alignment: [score]/100
Growth Potential: [score]/100
Overall Score: [score]/100

STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]

AREAS FOR IMPROVEMENT:
- [improvement area 1]
- [improvement area 2]
- [improvement area 3]

SPECIFIC FEEDBACK:
[Detailed feedback paragraph explaining the evaluation]

RECOMMENDATION:
[Strong Hire/Hire/No Hire with brief justification]
"""
        
        return prompt
    
    def _parse_evaluation_response(self, evaluation_text: str) -> Dict:
        """
        Parse evaluation response from AI.
        """
        evaluation = {
            'scores': {},
            'overall_score': 0,
            'strengths': [],
            'areas_for_improvement': [],
            'feedback': '',
            'recommendation': 'No Hire'
        }
        
        try:
            # Extract scores
            score_patterns = {
                'technical_accuracy': r'Technical Accuracy:\s*(\d+)',
                'communication_clarity': r'Communication Clarity:\s*(\d+)',
                'problem_solving_approach': r'Problem Solving Approach:\s*(\d+)',
                'experience_relevance': r'Experience Relevance:\s*(\d+)',
                'cultural_alignment': r'Cultural Alignment:\s*(\d+)',
                'growth_potential': r'Growth Potential:\s*(\d+)',
                'overall_score': r'Overall Score:\s*(\d+)'
            }
            
            for key, pattern in score_patterns.items():
                match = re.search(pattern, evaluation_text, re.IGNORECASE)
                if match:
                    score = int(match.group(1))
                    if key == 'overall_score':
                        evaluation['overall_score'] = score
                    else:
                        evaluation['scores'][key] = score
            
            # Calculate overall score if not provided
            if not evaluation['overall_score'] and evaluation['scores']:
                weights = {
                    'technical_accuracy': 0.25,
                    'communication_clarity': 0.20,
                    'problem_solving_approach': 0.20,
                    'experience_relevance': 0.15,
                    'cultural_alignment': 0.10,
                    'growth_potential': 0.10
                }
                
                weighted_sum = sum(
                    evaluation['scores'].get(key, 0) * weight
                    for key, weight in weights.items()
                )
                evaluation['overall_score'] = int(weighted_sum)
            
            # Extract strengths
            strengths_match = re.search(r'STRENGTHS:\s*(.*?)(?=AREAS FOR IMPROVEMENT:|$)', 
                                      evaluation_text, re.DOTALL | re.IGNORECASE)
            if strengths_match:
                strengths_text = strengths_match.group(1)
                strengths = [s.strip('- ').strip() for s in strengths_text.split('\n') if s.strip().startswith('-')]
                evaluation['strengths'] = [s for s in strengths if s]
            
            # Extract areas for improvement
            improvements_match = re.search(r'AREAS FOR IMPROVEMENT:\s*(.*?)(?=SPECIFIC FEEDBACK:|$)', 
                                         evaluation_text, re.DOTALL | re.IGNORECASE)
            if improvements_match:
                improvements_text = improvements_match.group(1)
                improvements = [s.strip('- ').strip() for s in improvements_text.split('\n') if s.strip().startswith('-')]
                evaluation['areas_for_improvement'] = [s for s in improvements if s]
            
            # Extract feedback
            feedback_match = re.search(r'SPECIFIC FEEDBACK:\s*(.*?)(?=RECOMMENDATION:|$)', 
                                     evaluation_text, re.DOTALL | re.IGNORECASE)
            if feedback_match:
                evaluation['feedback'] = feedback_match.group(1).strip()
            
            # Extract recommendation
            recommendation_match = re.search(r'RECOMMENDATION:\s*(.*?)$', 
                                           evaluation_text, re.DOTALL | re.IGNORECASE)
            if recommendation_match:
                recommendation_text = recommendation_match.group(1).strip()
                if 'strong hire' in recommendation_text.lower():
                    evaluation['recommendation'] = 'Strong Hire'
                elif 'hire' in recommendation_text.lower():
                    evaluation['recommendation'] = 'Hire'
                else:
                    evaluation['recommendation'] = 'No Hire'
            
        except Exception as e:
            logger.error(f"Error parsing evaluation response: {str(e)}")
        
        return evaluation
    
    def _get_fallback_questions(self, num_questions: int) -> List[Dict]:
        """
        Provide fallback questions if AI generation fails.
        """
        fallback_questions = [
            {
                'question': 'Tell me about your most challenging project and how you overcame the obstacles.',
                'category': 'behavioral',
                'type': 'problem_solving',
                'difficulty': 'medium',
                'question_number': 1,
                'estimated_time_minutes': 5
            },
            {
                'question': 'How do you stay updated with the latest technologies in your field?',
                'category': 'technical',
                'type': 'continuous_learning',
                'difficulty': 'easy',
                'question_number': 2,
                'estimated_time_minutes': 3
            },
            {
                'question': 'Describe a time when you had to work with a difficult team member.',
                'category': 'behavioral',
                'type': 'teamwork',
                'difficulty': 'medium',
                'question_number': 3,
                'estimated_time_minutes': 4
            },
            {
                'question': 'What interests you most about this role and our company?',
                'category': 'cultural_fit',
                'type': 'motivation',
                'difficulty': 'easy',
                'question_number': 4,
                'estimated_time_minutes': 3
            },
            {
                'question': 'How would you approach debugging a complex system issue?',
                'category': 'technical',
                'type': 'problem_solving',
                'difficulty': 'hard',
                'question_number': 5,
                'estimated_time_minutes': 6
            }
        ]
        
        return fallback_questions[:num_questions]
    
    def _get_fallback_category_questions(self, category: str, count: int) -> List[Dict]:
        """
        Get fallback questions for a specific category.
        """
        category_questions = {
            'technical': [
                'Explain the difference between SQL and NoSQL databases.',
                'How would you optimize a slow-performing web application?',
                'Describe your experience with version control systems.'
            ],
            'behavioral': [
                'Tell me about a time you had to learn a new technology quickly.',
                'Describe a situation where you had to meet a tight deadline.',
                'How do you handle constructive criticism?'
            ],
            'situational': [
                'How would you prioritize tasks when everything seems urgent?',
                'What would you do if you disagreed with your manager\'s technical decision?',
                'How would you handle a situation where a project is falling behind schedule?'
            ],
            'cultural_fit': [
                'What type of work environment do you thrive in?',
                'How do you prefer to receive feedback?',
                'What motivates you in your work?'
            ]
        }
        
        questions = category_questions.get(category, category_questions['behavioral'])
        
        return [
            {
                'question': q,
                'category': category,
                'type': category,
                'difficulty': 'medium',
                'estimated_time_minutes': 4
            }
            for q in questions[:count]
        ]
    
    def _get_fallback_evaluation(self) -> Dict:
        """
        Provide fallback evaluation if AI evaluation fails.
        """
        return {
            'scores': {
                'technical_accuracy': 70,
                'communication_clarity': 70,
                'problem_solving_approach': 70,
                'experience_relevance': 70,
                'cultural_alignment': 70,
                'growth_potential': 70
            },
            'overall_score': 70,
            'strengths': ['Response provided', 'Attempted to answer question'],
            'areas_for_improvement': ['Could provide more specific examples', 'Could elaborate on technical details'],
            'feedback': 'Unable to provide detailed evaluation due to technical issues. Manual review recommended.',
            'recommendation': 'Manual Review Required'
        }

