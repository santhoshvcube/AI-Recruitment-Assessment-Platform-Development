import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import statistics
from src.services.nlp_analyzer import NLPAnalyzer
from src.services.interview_simulator import InterviewSimulator

logger = logging.getLogger(__name__)

class AssessmentEngine:
    """
    Comprehensive assessment engine that combines multiple evaluation methods
    to provide holistic candidate assessment with quantifiable metrics.
    """
    
    def __init__(self):
        self.nlp_analyzer = NLPAnalyzer()
        self.interview_simulator = InterviewSimulator()
        
        # Assessment weights for different components
        self.assessment_weights = {
            'resume_analysis': 0.30,
            'skill_match': 0.25,
            'interview_performance': 0.35,
            'experience_relevance': 0.10
        }
        
        # Score thresholds for recommendations
        self.score_thresholds = {
            'strong_hire': 85,
            'hire': 70,
            'maybe': 55,
            'no_hire': 0
        }
        
        # Cultural fit indicators
        self.cultural_fit_factors = {
            'communication_style': 0.25,
            'collaboration_indicators': 0.25,
            'adaptability_signals': 0.20,
            'leadership_potential': 0.15,
            'learning_agility': 0.15
        }
    
    def conduct_comprehensive_assessment(self, 
                                       candidate_data: Dict,
                                       job_description: Dict,
                                       interview_responses: Optional[List[Dict]] = None) -> Dict:
        """
        Conduct a comprehensive multi-dimensional assessment of a candidate.
        
        Args:
            candidate_data: Complete candidate information including resume analysis
            job_description: Job requirements and description
            interview_responses: Optional interview responses for evaluation
            
        Returns:
            Comprehensive assessment report with scores and recommendations
        """
        try:
            assessment_report = {
                'candidate_id': candidate_data.get('id'),
                'job_id': job_description.get('id'),
                'assessment_timestamp': datetime.utcnow().isoformat(),
                'overall_score': 0,
                'component_scores': {},
                'detailed_analysis': {},
                'recommendations': {},
                'risk_factors': [],
                'strengths': [],
                'development_areas': [],
                'hiring_recommendation': 'no_hire',
                'confidence_level': 0
            }
            
            # 1. Resume and Skills Analysis
            resume_score = self._assess_resume_quality(candidate_data)
            assessment_report['component_scores']['resume_analysis'] = resume_score
            
            # 2. Skill Matching Analysis
            skill_match_score = self._assess_skill_match(candidate_data, job_description)
            assessment_report['component_scores']['skill_match'] = skill_match_score
            
            # 3. Experience Relevance Analysis
            experience_score = self._assess_experience_relevance(candidate_data, job_description)
            assessment_report['component_scores']['experience_relevance'] = experience_score
            
            # 4. Interview Performance Analysis (if available)
            interview_score = 0
            if interview_responses:
                interview_score = self._assess_interview_performance(interview_responses)
                assessment_report['component_scores']['interview_performance'] = interview_score
            
            # 5. Calculate Overall Score
            overall_score = self._calculate_overall_score(assessment_report['component_scores'])
            assessment_report['overall_score'] = overall_score
            
            # 6. Generate Detailed Analysis
            assessment_report['detailed_analysis'] = self._generate_detailed_analysis(
                candidate_data, job_description, assessment_report['component_scores']
            )
            
            # 7. Cultural Fit Assessment
            cultural_fit_score = self._assess_cultural_fit(candidate_data, interview_responses)
            assessment_report['component_scores']['cultural_fit'] = cultural_fit_score
            
            # 8. Risk Assessment
            assessment_report['risk_factors'] = self._identify_risk_factors(
                candidate_data, assessment_report['component_scores']
            )
            
            # 9. Generate Recommendations
            assessment_report['recommendations'] = self._generate_recommendations(
                assessment_report['overall_score'], 
                assessment_report['component_scores'],
                assessment_report['detailed_analysis']
            )
            
            # 10. Determine Hiring Recommendation
            assessment_report['hiring_recommendation'] = self._determine_hiring_recommendation(
                overall_score, assessment_report['risk_factors']
            )
            
            # 11. Calculate Confidence Level
            assessment_report['confidence_level'] = self._calculate_confidence_level(
                assessment_report['component_scores'], interview_responses is not None
            )
            
            # 12. Extract Strengths and Development Areas
            strengths, development_areas = self._extract_strengths_and_development_areas(
                assessment_report['detailed_analysis'], assessment_report['component_scores']
            )
            assessment_report['strengths'] = strengths
            assessment_report['development_areas'] = development_areas
            
            return assessment_report
            
        except Exception as e:
            logger.error(f"Error conducting comprehensive assessment: {str(e)}")
            return self._get_fallback_assessment()
    
    def _assess_resume_quality(self, candidate_data: Dict) -> Dict:
        """
        Assess the quality and completeness of the resume.
        """
        resume_text = candidate_data.get('resume_text', '')
        extracted_skills = candidate_data.get('extracted_skills', {})
        extracted_experience = candidate_data.get('extracted_experience', {})
        extracted_education = candidate_data.get('extracted_education', {})
        
        score_components = {
            'completeness': 0,
            'skill_diversity': 0,
            'experience_depth': 0,
            'education_relevance': 0,
            'presentation_quality': 0
        }
        
        # Assess completeness (0-100)
        required_sections = ['contact', 'experience', 'skills', 'education']
        sections_present = 0
        
        if candidate_data.get('email'):
            sections_present += 1
        if extracted_experience.get('job_titles'):
            sections_present += 1
        if extracted_skills.get('all_skills'):
            sections_present += 1
        if extracted_education.get('degrees'):
            sections_present += 1
            
        score_components['completeness'] = (sections_present / len(required_sections)) * 100
        
        # Assess skill diversity (0-100)
        all_skills = extracted_skills.get('all_skills', [])
        technical_skills = extracted_skills.get('technical_skills', {})
        soft_skills = extracted_skills.get('soft_skills', [])
        
        skill_categories = sum(1 for category in technical_skills.values() if category)
        skill_diversity_score = min(100, (len(all_skills) * 5) + (skill_categories * 10))
        score_components['skill_diversity'] = skill_diversity_score
        
        # Assess experience depth (0-100)
        total_years = extracted_experience.get('total_years', 0)
        job_titles = extracted_experience.get('job_titles', [])
        companies = extracted_experience.get('companies', [])
        
        experience_depth = min(100, (total_years * 10) + (len(job_titles) * 5) + (len(companies) * 3))
        score_components['experience_depth'] = experience_depth
        
        # Assess education relevance (0-100)
        education_level = extracted_education.get('education_level', 'high_school')
        education_scores = {
            'doctorate': 100,
            'masters': 85,
            'bachelors': 70,
            'associates': 55,
            'high_school': 40
        }
        score_components['education_relevance'] = education_scores.get(education_level, 40)
        
        # Assess presentation quality (0-100)
        presentation_score = 70  # Base score
        
        # Check for formatting indicators
        if len(resume_text) > 500:  # Adequate length
            presentation_score += 10
        if len(resume_text.split('\n')) > 20:  # Good structure
            presentation_score += 10
        if any(char in resume_text for char in ['•', '▪', '◦']):  # Bullet points
            presentation_score += 10
            
        score_components['presentation_quality'] = min(100, presentation_score)
        
        # Calculate weighted average
        weights = {
            'completeness': 0.25,
            'skill_diversity': 0.25,
            'experience_depth': 0.25,
            'education_relevance': 0.15,
            'presentation_quality': 0.10
        }
        
        overall_score = sum(score_components[key] * weights[key] for key in weights)
        
        return {
            'overall_score': round(overall_score, 2),
            'component_scores': score_components,
            'analysis': self._generate_resume_analysis(score_components)
        }
    
    def _assess_skill_match(self, candidate_data: Dict, job_description: Dict) -> Dict:
        """
        Assess how well candidate skills match job requirements.
        """
        candidate_skills = candidate_data.get('extracted_skills', {}).get('all_skills', [])
        required_skills = job_description.get('required_skills', [])
        preferred_skills = job_description.get('preferred_skills', [])
        
        # Calculate match scores
        required_match = self.nlp_analyzer.calculate_job_match_score(candidate_skills, required_skills)
        preferred_match = self.nlp_analyzer.calculate_job_match_score(candidate_skills, preferred_skills)
        
        # Weight required skills more heavily
        overall_match_score = (required_match['match_score'] * 0.7) + (preferred_match['match_score'] * 0.3)
        
        # Assess skill level and depth
        technical_skills = candidate_data.get('extracted_skills', {}).get('technical_skills', {})
        skill_depth_score = self._assess_skill_depth(technical_skills, required_skills)
        
        # Combine scores
        final_score = (overall_match_score * 0.8) + (skill_depth_score * 0.2)
        
        return {
            'overall_score': round(final_score, 2),
            'required_skills_match': required_match,
            'preferred_skills_match': preferred_match,
            'skill_depth_score': skill_depth_score,
            'analysis': {
                'strong_matches': required_match['matched_skills'][:5],
                'missing_critical': required_match['missing_skills'][:5],
                'additional_value': [skill for skill in candidate_skills 
                                  if skill not in required_skills + preferred_skills][:5]
            }
        }
    
    def _assess_experience_relevance(self, candidate_data: Dict, job_description: Dict) -> Dict:
        """
        Assess the relevance of candidate's experience to the job.
        """
        experience_data = candidate_data.get('extracted_experience', {})
        job_title = job_description.get('title', '')
        job_level = job_description.get('experience_level', 'mid')
        
        score_components = {
            'years_alignment': 0,
            'role_relevance': 0,
            'industry_match': 0,
            'progression_quality': 0,
            'leadership_experience': 0
        }
        
        # Assess years alignment
        total_years = experience_data.get('total_years', 0)
        experience_level = experience_data.get('experience_level', 'entry')
        
        level_requirements = {
            'entry': (0, 2),
            'junior': (1, 3),
            'mid': (3, 7),
            'senior': (5, 12),
            'executive': (8, 20)
        }
        
        min_years, max_years = level_requirements.get(job_level, (3, 7))
        if min_years <= total_years <= max_years:
            score_components['years_alignment'] = 100
        elif total_years > max_years:
            score_components['years_alignment'] = max(70, 100 - ((total_years - max_years) * 5))
        else:
            score_components['years_alignment'] = (total_years / min_years) * 100 if min_years > 0 else 0
        
        # Assess role relevance
        job_titles = experience_data.get('job_titles', [])
        role_relevance_score = self._calculate_role_relevance(job_titles, job_title)
        score_components['role_relevance'] = role_relevance_score
        
        # Assess career progression
        progression_data = experience_data.get('career_progression', {})
        progression_score = 70  # Base score
        
        if progression_data.get('shows_growth'):
            progression_score += 20
        if progression_data.get('leadership_progression'):
            progression_score += 10
            
        score_components['progression_quality'] = min(100, progression_score)
        
        # Assess leadership experience
        leadership_score = 50  # Base score
        if progression_data.get('leadership_progression'):
            leadership_score += 30
        if any('lead' in title.lower() or 'manager' in title.lower() 
               for title in job_titles):
            leadership_score += 20
            
        score_components['leadership_experience'] = min(100, leadership_score)
        
        # Industry match (simplified - could be enhanced with industry classification)
        score_components['industry_match'] = 75  # Default moderate match
        
        # Calculate weighted average
        weights = {
            'years_alignment': 0.30,
            'role_relevance': 0.30,
            'progression_quality': 0.20,
            'leadership_experience': 0.10,
            'industry_match': 0.10
        }
        
        overall_score = sum(score_components[key] * weights[key] for key in weights)
        
        return {
            'overall_score': round(overall_score, 2),
            'component_scores': score_components,
            'analysis': {
                'experience_level_match': experience_level == job_level,
                'years_vs_requirement': f"{total_years} years (requirement: {min_years}-{max_years})",
                'career_highlights': job_titles[:3],
                'progression_indicators': progression_data
            }
        }
    
    def _assess_interview_performance(self, interview_responses: List[Dict]) -> Dict:
        """
        Assess overall interview performance from individual response evaluations.
        """
        if not interview_responses:
            return {'overall_score': 0, 'analysis': 'No interview data available'}
        
        # Aggregate scores from individual responses
        all_scores = []
        category_scores = {}
        
        for response in interview_responses:
            evaluation = response.get('evaluation', {})
            overall_score = evaluation.get('overall_score', 0)
            all_scores.append(overall_score)
            
            # Aggregate by category
            category = response.get('question', {}).get('category', 'unknown')
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(overall_score)
        
        # Calculate overall interview score
        overall_interview_score = statistics.mean(all_scores) if all_scores else 0
        
        # Calculate category averages
        category_averages = {
            category: statistics.mean(scores)
            for category, scores in category_scores.items()
        }
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        for response in interview_responses:
            evaluation = response.get('evaluation', {})
            strengths.extend(evaluation.get('strengths', []))
            weaknesses.extend(evaluation.get('areas_for_improvement', []))
        
        # Remove duplicates and limit
        strengths = list(set(strengths))[:5]
        weaknesses = list(set(weaknesses))[:5]
        
        return {
            'overall_score': round(overall_interview_score, 2),
            'category_scores': category_averages,
            'total_questions': len(interview_responses),
            'analysis': {
                'strongest_categories': sorted(category_averages.items(), 
                                             key=lambda x: x[1], reverse=True)[:3],
                'improvement_areas': sorted(category_averages.items(), 
                                          key=lambda x: x[1])[:3],
                'key_strengths': strengths,
                'development_needs': weaknesses
            }
        }
    
    def _assess_cultural_fit(self, candidate_data: Dict, interview_responses: Optional[List[Dict]]) -> Dict:
        """
        Assess cultural fit based on communication style and responses.
        """
        cultural_fit_score = 70  # Base score
        
        analysis = {
            'communication_style': 'professional',
            'collaboration_indicators': [],
            'adaptability_signals': [],
            'values_alignment': 'moderate'
        }
        
        # Analyze communication from interview responses
        if interview_responses:
            communication_scores = []
            for response in interview_responses:
                evaluation = response.get('evaluation', {})
                comm_score = evaluation.get('scores', {}).get('communication_clarity', 70)
                communication_scores.append(comm_score)
                
                # Extract cultural indicators from feedback
                feedback = evaluation.get('feedback', '').lower()
                if 'collaborative' in feedback or 'team' in feedback:
                    analysis['collaboration_indicators'].append('Shows teamwork orientation')
                if 'adaptable' in feedback or 'flexible' in feedback:
                    analysis['adaptability_signals'].append('Demonstrates adaptability')
            
            if communication_scores:
                avg_comm_score = statistics.mean(communication_scores)
                cultural_fit_score = (cultural_fit_score + avg_comm_score) / 2
        
        # Analyze experience for cultural indicators
        experience_data = candidate_data.get('extracted_experience', {})
        responsibilities = experience_data.get('responsibilities', [])
        
        for resp in responsibilities:
            resp_lower = resp.lower()
            if any(word in resp_lower for word in ['team', 'collaborate', 'mentor']):
                analysis['collaboration_indicators'].append('Experience with team collaboration')
            if any(word in resp_lower for word in ['adapt', 'change', 'transform']):
                analysis['adaptability_signals'].append('Experience with change management')
        
        return {
            'overall_score': round(cultural_fit_score, 2),
            'analysis': analysis
        }
    
    def _calculate_overall_score(self, component_scores: Dict) -> float:
        """
        Calculate weighted overall assessment score.
        """
        total_score = 0
        total_weight = 0
        
        for component, weight in self.assessment_weights.items():
            if component in component_scores:
                score_data = component_scores[component]
                if isinstance(score_data, dict):
                    score = score_data.get('overall_score', 0)
                else:
                    score = score_data
                
                total_score += score * weight
                total_weight += weight
        
        return round(total_score / total_weight if total_weight > 0 else 0, 2)
    
    def _identify_risk_factors(self, candidate_data: Dict, component_scores: Dict) -> List[Dict]:
        """
        Identify potential risk factors in the candidate profile.
        """
        risk_factors = []
        
        # Employment gaps
        experience_data = candidate_data.get('extracted_experience', {})
        gaps = experience_data.get('employment_gaps', [])
        
        for gap_start, gap_end in gaps:
            gap_length = gap_end - gap_start
            if gap_length > 1:  # Gap longer than 1 year
                risk_factors.append({
                    'type': 'employment_gap',
                    'severity': 'medium' if gap_length <= 2 else 'high',
                    'description': f'Employment gap of {gap_length} years ({gap_start}-{gap_end})',
                    'mitigation': 'Discuss reasons for gap and activities during this period'
                })
        
        # Skill gaps
        skill_match = component_scores.get('skill_match', {})
        if isinstance(skill_match, dict):
            missing_skills = skill_match.get('required_skills_match', {}).get('missing_skills', [])
            if missing_skills:
                risk_factors.append({
                    'type': 'skill_gap',
                    'severity': 'medium',
                    'description': f'Missing required skills: {", ".join(missing_skills[:3])}',
                    'mitigation': 'Assess learning ability and provide training plan'
                })
        
        # Overqualification
        experience_relevance = component_scores.get('experience_relevance', {})
        if isinstance(experience_relevance, dict):
            years_info = experience_relevance.get('analysis', {}).get('years_vs_requirement', '')
            if 'years' in years_info:
                try:
                    actual_years = int(years_info.split()[0])
                    if actual_years > 15:  # Potentially overqualified
                        risk_factors.append({
                            'type': 'overqualification',
                            'severity': 'low',
                            'description': 'Candidate may be overqualified for the role',
                            'mitigation': 'Discuss career goals and long-term commitment'
                        })
                except (ValueError, IndexError):
                    pass
        
        # Low interview performance
        interview_score = component_scores.get('interview_performance', {})
        if isinstance(interview_score, dict):
            score = interview_score.get('overall_score', 100)
            if score < 60:
                risk_factors.append({
                    'type': 'interview_performance',
                    'severity': 'high',
                    'description': 'Below-average interview performance',
                    'mitigation': 'Consider additional interview rounds or practical assessments'
                })
        
        return risk_factors
    
    def _generate_recommendations(self, overall_score: float, component_scores: Dict, detailed_analysis: Dict) -> Dict:
        """
        Generate actionable recommendations based on assessment results.
        """
        recommendations = {
            'hiring_decision': '',
            'next_steps': [],
            'development_plan': [],
            'onboarding_focus': [],
            'follow_up_questions': []
        }
        
        # Hiring decision recommendation
        if overall_score >= self.score_thresholds['strong_hire']:
            recommendations['hiring_decision'] = 'Strong Hire - Excellent candidate with minimal risk'
            recommendations['next_steps'] = [
                'Proceed with offer preparation',
                'Conduct reference checks',
                'Prepare comprehensive onboarding plan'
            ]
        elif overall_score >= self.score_thresholds['hire']:
            recommendations['hiring_decision'] = 'Hire - Good candidate with manageable development needs'
            recommendations['next_steps'] = [
                'Conduct final interview round',
                'Verify key skills through practical assessment',
                'Prepare targeted development plan'
            ]
        elif overall_score >= self.score_thresholds['maybe']:
            recommendations['hiring_decision'] = 'Maybe - Candidate shows potential but has significant gaps'
            recommendations['next_steps'] = [
                'Conduct additional technical assessment',
                'Interview with senior team members',
                'Evaluate cultural fit more thoroughly'
            ]
        else:
            recommendations['hiring_decision'] = 'No Hire - Candidate does not meet minimum requirements'
            recommendations['next_steps'] = [
                'Provide constructive feedback',
                'Consider for future opportunities if applicable',
                'Document assessment for learning purposes'
            ]
        
        # Development plan based on weak areas
        for component, score_data in component_scores.items():
            if isinstance(score_data, dict):
                score = score_data.get('overall_score', 0)
            else:
                score = score_data
                
            if score < 70:  # Below threshold
                if component == 'skill_match':
                    recommendations['development_plan'].append(
                        'Technical skills training in missing areas'
                    )
                elif component == 'interview_performance':
                    recommendations['development_plan'].append(
                        'Communication and presentation skills development'
                    )
                elif component == 'experience_relevance':
                    recommendations['development_plan'].append(
                        'Mentoring and guidance in role-specific responsibilities'
                    )
        
        return recommendations
    
    def _determine_hiring_recommendation(self, overall_score: float, risk_factors: List[Dict]) -> str:
        """
        Determine final hiring recommendation considering score and risks.
        """
        # Base recommendation on score
        if overall_score >= self.score_thresholds['strong_hire']:
            base_recommendation = 'strong_hire'
        elif overall_score >= self.score_thresholds['hire']:
            base_recommendation = 'hire'
        elif overall_score >= self.score_thresholds['maybe']:
            base_recommendation = 'maybe'
        else:
            base_recommendation = 'no_hire'
        
        # Adjust for high-severity risk factors
        high_risk_count = sum(1 for risk in risk_factors if risk.get('severity') == 'high')
        
        if high_risk_count >= 2:
            # Downgrade recommendation
            if base_recommendation == 'strong_hire':
                return 'hire'
            elif base_recommendation == 'hire':
                return 'maybe'
            else:
                return 'no_hire'
        
        return base_recommendation
    
    def _calculate_confidence_level(self, component_scores: Dict, has_interview_data: bool) -> float:
        """
        Calculate confidence level in the assessment.
        """
        base_confidence = 70
        
        # Increase confidence if we have interview data
        if has_interview_data:
            base_confidence += 20
        
        # Increase confidence based on data completeness
        complete_components = sum(1 for score in component_scores.values() 
                                if isinstance(score, dict) and score.get('overall_score', 0) > 0)
        
        completeness_bonus = (complete_components / len(self.assessment_weights)) * 10
        
        return min(100, base_confidence + completeness_bonus)
    
    def _extract_strengths_and_development_areas(self, detailed_analysis: Dict, component_scores: Dict) -> Tuple[List[str], List[str]]:
        """
        Extract key strengths and development areas from the assessment.
        """
        strengths = []
        development_areas = []
        
        # Analyze component scores for strengths and weaknesses
        for component, score_data in component_scores.items():
            if isinstance(score_data, dict):
                score = score_data.get('overall_score', 0)
                analysis = score_data.get('analysis', {})
                
                if score >= 80:  # Strong area
                    if component == 'skill_match':
                        strengths.append(f"Strong technical skill alignment ({score}%)")
                    elif component == 'experience_relevance':
                        strengths.append(f"Highly relevant experience ({score}%)")
                    elif component == 'interview_performance':
                        strengths.append(f"Excellent interview performance ({score}%)")
                    elif component == 'resume_analysis':
                        strengths.append(f"Well-structured professional profile ({score}%)")
                
                elif score < 60:  # Development area
                    if component == 'skill_match':
                        development_areas.append("Technical skills gap in key areas")
                    elif component == 'experience_relevance':
                        development_areas.append("Limited relevant experience")
                    elif component == 'interview_performance':
                        development_areas.append("Interview communication needs improvement")
                    elif component == 'resume_analysis':
                        development_areas.append("Professional presentation could be enhanced")
        
        return strengths[:5], development_areas[:5]  # Limit to top 5 each
    
    def _generate_detailed_analysis(self, candidate_data: Dict, job_description: Dict, component_scores: Dict) -> Dict:
        """
        Generate detailed analysis combining all assessment components.
        """
        return {
            'candidate_summary': {
                'name': candidate_data.get('name', 'Unknown'),
                'experience_level': candidate_data.get('extracted_experience', {}).get('experience_level', 'unknown'),
                'total_years': candidate_data.get('extracted_experience', {}).get('total_years', 0),
                'key_skills': candidate_data.get('extracted_skills', {}).get('all_skills', [])[:10],
                'education_level': candidate_data.get('extracted_education', {}).get('education_level', 'unknown')
            },
            'role_alignment': {
                'position': job_description.get('title', 'Unknown'),
                'skill_match_percentage': component_scores.get('skill_match', {}).get('overall_score', 0),
                'experience_alignment': component_scores.get('experience_relevance', {}).get('overall_score', 0),
                'cultural_fit_score': component_scores.get('cultural_fit', {}).get('overall_score', 0)
            },
            'assessment_summary': {
                'total_components_evaluated': len(component_scores),
                'highest_scoring_area': max(component_scores.items(), 
                                          key=lambda x: x[1].get('overall_score', 0) if isinstance(x[1], dict) else x[1])[0],
                'lowest_scoring_area': min(component_scores.items(), 
                                         key=lambda x: x[1].get('overall_score', 0) if isinstance(x[1], dict) else x[1])[0]
            }
        }
    
    def _generate_resume_analysis(self, score_components: Dict) -> str:
        """
        Generate textual analysis of resume quality.
        """
        analysis_parts = []
        
        if score_components['completeness'] >= 80:
            analysis_parts.append("Resume contains all essential sections")
        elif score_components['completeness'] >= 60:
            analysis_parts.append("Resume is mostly complete with minor gaps")
        else:
            analysis_parts.append("Resume is missing key sections")
        
        if score_components['skill_diversity'] >= 80:
            analysis_parts.append("demonstrates diverse technical competencies")
        elif score_components['skill_diversity'] >= 60:
            analysis_parts.append("shows adequate technical skills")
        else:
            analysis_parts.append("has limited technical skill representation")
        
        if score_components['experience_depth'] >= 80:
            analysis_parts.append("and substantial professional experience")
        elif score_components['experience_depth'] >= 60:
            analysis_parts.append("and moderate professional experience")
        else:
            analysis_parts.append("but limited professional experience")
        
        return ". ".join(analysis_parts).capitalize() + "."
    
    def _assess_skill_depth(self, technical_skills: Dict, required_skills: List[str]) -> float:
        """
        Assess the depth and breadth of technical skills.
        """
        if not technical_skills or not required_skills:
            return 50
        
        # Count skills in different categories
        total_categories = len(technical_skills)
        populated_categories = sum(1 for skills in technical_skills.values() if skills)
        
        # Calculate breadth score
        breadth_score = (populated_categories / total_categories) * 100 if total_categories > 0 else 0
        
        # Calculate depth score based on total skills
        total_skills = sum(len(skills) for skills in technical_skills.values())
        depth_score = min(100, total_skills * 5)  # 5 points per skill, max 100
        
        # Combine breadth and depth
        return (breadth_score * 0.4) + (depth_score * 0.6)
    
    def _calculate_role_relevance(self, job_titles: List[str], target_role: str) -> float:
        """
        Calculate relevance of previous job titles to target role.
        """
        if not job_titles or not target_role:
            return 50
        
        target_keywords = target_role.lower().split()
        relevance_scores = []
        
        for title in job_titles:
            title_keywords = title.lower().split()
            common_keywords = set(target_keywords) & set(title_keywords)
            relevance = (len(common_keywords) / len(target_keywords)) * 100
            relevance_scores.append(relevance)
        
        # Return the highest relevance score
        return max(relevance_scores) if relevance_scores else 50
    
    def _get_fallback_assessment(self) -> Dict:
        """
        Provide fallback assessment if main assessment fails.
        """
        return {
            'overall_score': 50,
            'component_scores': {
                'resume_analysis': {'overall_score': 50},
                'skill_match': {'overall_score': 50},
                'experience_relevance': {'overall_score': 50}
            },
            'detailed_analysis': {
                'error': 'Assessment could not be completed due to technical issues'
            },
            'recommendations': {
                'hiring_decision': 'Manual Review Required',
                'next_steps': ['Conduct manual assessment', 'Review technical issues']
            },
            'risk_factors': [
                {
                    'type': 'technical_error',
                    'severity': 'high',
                    'description': 'Automated assessment failed',
                    'mitigation': 'Conduct manual review'
                }
            ],
            'strengths': ['Assessment data available'],
            'development_areas': ['Technical assessment needed'],
            'hiring_recommendation': 'manual_review',
            'confidence_level': 20
        }

