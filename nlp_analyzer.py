import spacy
import re
from typing import Dict, List, Set, Tuple, Optional
from collections import Counter
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NLPAnalyzer:
    """
    Advanced Natural Language Processing service for resume analysis.
    Handles skill extraction, experience evaluation, and semantic analysis.
    """
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spaCy English model not found. Please install with: python -m spacy download en_core_web_sm")
            raise
        
        # Technical skills database
        self.technical_skills = {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 
                'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell',
                'bash', 'powershell', 'sql', 'html', 'css', 'sass', 'less'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring',
                'spring boot', 'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'tailwind',
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 
                'sql server', 'sqlite', 'cassandra', 'dynamodb', 'firebase'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'digitalocean', 'linode',
                'cloudflare', 'vercel', 'netlify'
            ],
            'tools_technologies': [
                'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab', 'bitbucket',
                'jira', 'confluence', 'slack', 'teams', 'figma', 'sketch', 'photoshop',
                'illustrator', 'postman', 'insomnia', 'webpack', 'vite', 'babel'
            ],
            'methodologies': [
                'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd', 'microservices',
                'rest api', 'graphql', 'soap', 'mvc', 'mvvm', 'solid principles'
            ]
        }
        
        # Soft skills database
        self.soft_skills = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
            'creativity', 'adaptability', 'time management', 'project management', 'mentoring',
            'collaboration', 'critical thinking', 'decision making', 'negotiation', 'presentation',
            'public speaking', 'writing', 'research', 'organization', 'attention to detail'
        ]
        
        # Experience level indicators
        self.experience_indicators = {
            'junior': ['junior', 'entry level', 'associate', 'intern', 'trainee', 'graduate'],
            'mid': ['mid level', 'intermediate', 'experienced', 'specialist', 'analyst'],
            'senior': ['senior', 'lead', 'principal', 'staff', 'expert', 'architect'],
            'executive': ['manager', 'director', 'vp', 'vice president', 'ceo', 'cto', 'head of']
        }
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract technical and soft skills from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary categorizing found skills
        """
        text_lower = text.lower()
        doc = self.nlp(text)
        
        found_skills = {
            'technical_skills': {
                'programming_languages': [],
                'frameworks_libraries': [],
                'databases': [],
                'cloud_platforms': [],
                'tools_technologies': [],
                'methodologies': []
            },
            'soft_skills': [],
            'certifications': [],
            'all_skills': []
        }
        
        # Extract technical skills
        for category, skills_list in self.technical_skills.items():
            for skill in skills_list:
                if self._find_skill_in_text(skill, text_lower):
                    found_skills['technical_skills'][category].append(skill)
                    found_skills['all_skills'].append(skill)
        
        # Extract soft skills
        for skill in self.soft_skills:
            if self._find_skill_in_text(skill, text_lower):
                found_skills['soft_skills'].append(skill)
                found_skills['all_skills'].append(skill)
        
        # Extract certifications using NER and patterns
        certifications = self._extract_certifications(text, doc)
        found_skills['certifications'] = certifications
        
        # Remove duplicates
        for category in found_skills['technical_skills']:
            found_skills['technical_skills'][category] = list(set(found_skills['technical_skills'][category]))
        found_skills['soft_skills'] = list(set(found_skills['soft_skills']))
        found_skills['all_skills'] = list(set(found_skills['all_skills']))
        
        return found_skills
    
    def _find_skill_in_text(self, skill: str, text: str) -> bool:
        """
        Find skill in text using various matching strategies.
        """
        # Exact match
        if skill in text:
            return True
        
        # Word boundary match
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
        # Handle special cases (e.g., "node.js" vs "node")
        if '.' in skill:
            skill_without_dot = skill.replace('.', '')
            if skill_without_dot in text:
                return True
        
        return False
    
    def _extract_certifications(self, text: str, doc) -> List[str]:
        """
        Extract certifications using NER and pattern matching.
        """
        certifications = []
        
        # Common certification patterns
        cert_patterns = [
            r'certified\s+[\w\s]+',
            r'[\w\s]+\s+certified',
            r'[\w\s]+\s+certification',
            r'aws\s+[\w\s]+',
            r'microsoft\s+[\w\s]+',
            r'google\s+[\w\s]+',
            r'cisco\s+[\w\s]+',
            r'oracle\s+[\w\s]+',
            r'pmp\b',
            r'cissp\b',
            r'cisa\b',
            r'cism\b'
        ]
        
        for pattern in cert_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                cert = match.group().strip()
                if len(cert) > 3 and len(cert) < 100:  # Reasonable length
                    certifications.append(cert)
        
        return list(set(certifications))
    
    def analyze_experience(self, text: str) -> Dict[str, any]:
        """
        Analyze work experience from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with experience analysis
        """
        doc = self.nlp(text)
        
        experience_analysis = {
            'total_years': 0,
            'experience_level': 'entry',
            'job_titles': [],
            'companies': [],
            'responsibilities': [],
            'achievements': [],
            'career_progression': [],
            'employment_gaps': []
        }
        
        # Extract job titles and companies using NER
        organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        experience_analysis['companies'] = list(set(organizations))
        
        # Extract dates and calculate experience
        dates = self._extract_dates(text)
        if dates:
            experience_analysis['total_years'] = self._calculate_total_experience(dates)
            experience_analysis['employment_gaps'] = self._identify_gaps(dates)
        
        # Determine experience level
        experience_analysis['experience_level'] = self._determine_experience_level(
            text, experience_analysis['total_years']
        )
        
        # Extract job titles
        job_titles = self._extract_job_titles(text)
        experience_analysis['job_titles'] = job_titles
        
        # Extract responsibilities and achievements
        responsibilities, achievements = self._extract_responsibilities_achievements(text)
        experience_analysis['responsibilities'] = responsibilities
        experience_analysis['achievements'] = achievements
        
        # Analyze career progression
        experience_analysis['career_progression'] = self._analyze_career_progression(job_titles)
        
        return experience_analysis
    
    def _extract_dates(self, text: str) -> List[Tuple[int, int]]:
        """
        Extract date ranges from text.
        """
        date_patterns = [
            r'(\d{4})\s*[-–—]\s*(\d{4})',
            r'(\d{4})\s*[-–—]\s*present',
            r'(\d{1,2}/\d{4})\s*[-–—]\s*(\d{1,2}/\d{4})',
            r'(\d{1,2}/\d{4})\s*[-–—]\s*present',
            r'(\w+\s+\d{4})\s*[-–—]\s*(\w+\s+\d{4})',
            r'(\w+\s+\d{4})\s*[-–—]\s*present'
        ]
        
        dates = []
        current_year = datetime.now().year
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start_str, end_str = match.groups()
                
                try:
                    # Extract year from start date
                    start_year = int(re.search(r'\d{4}', start_str).group())
                    
                    # Extract year from end date
                    if 'present' in end_str.lower():
                        end_year = current_year
                    else:
                        end_year = int(re.search(r'\d{4}', end_str).group())
                    
                    if start_year <= end_year <= current_year:
                        dates.append((start_year, end_year))
                        
                except (ValueError, AttributeError):
                    continue
        
        return dates
    
    def _calculate_total_experience(self, dates: List[Tuple[int, int]]) -> float:
        """
        Calculate total years of experience from date ranges.
        """
        if not dates:
            return 0
        
        # Sort dates and merge overlapping periods
        sorted_dates = sorted(dates)
        merged_dates = []
        
        for start, end in sorted_dates:
            if not merged_dates or start > merged_dates[-1][1]:
                merged_dates.append((start, end))
            else:
                # Merge overlapping periods
                merged_dates[-1] = (merged_dates[-1][0], max(merged_dates[-1][1], end))
        
        # Calculate total years
        total_years = sum(end - start for start, end in merged_dates)
        return total_years
    
    def _identify_gaps(self, dates: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Identify employment gaps.
        """
        if len(dates) < 2:
            return []
        
        sorted_dates = sorted(dates)
        gaps = []
        
        for i in range(len(sorted_dates) - 1):
            current_end = sorted_dates[i][1]
            next_start = sorted_dates[i + 1][0]
            
            if next_start > current_end + 1:  # Gap of more than 1 year
                gaps.append((current_end, next_start))
        
        return gaps
    
    def _determine_experience_level(self, text: str, total_years: float) -> str:
        """
        Determine experience level based on years and job titles.
        """
        text_lower = text.lower()
        
        # Check for explicit level indicators in text
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return level
        
        # Determine by years of experience
        if total_years < 2:
            return 'junior'
        elif total_years < 5:
            return 'mid'
        elif total_years < 10:
            return 'senior'
        else:
            return 'executive'
    
    def _extract_job_titles(self, text: str) -> List[str]:
        """
        Extract job titles from resume text.
        """
        job_title_patterns = [
            r'(?:^|\n)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator|Assistant|Director|Lead|Senior|Junior|Principal|Staff)))\s*(?:\n|$)',
            r'(?:Position|Role|Title):\s*([^\n]+)',
            r'(?:as|as a|as an)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator|Assistant|Director|Lead|Senior|Junior|Principal|Staff)))'
        ]
        
        job_titles = []
        
        for pattern in job_title_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                title = match.group(1).strip()
                if len(title) > 3 and len(title) < 100:
                    job_titles.append(title)
        
        return list(set(job_titles))
    
    def _extract_responsibilities_achievements(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Extract responsibilities and achievements from resume text.
        """
        responsibilities = []
        achievements = []
        
        # Patterns for responsibilities
        resp_patterns = [
            r'[•·▪▫◦‣⁃]\s*([^•·▪▫◦‣⁃\n]+)',
            r'^\s*[-*]\s*([^-*\n]+)',
            r'(?:Responsible for|Responsibilities include|Duties include):\s*([^\n]+)'
        ]
        
        # Patterns for achievements
        achievement_keywords = ['achieved', 'improved', 'increased', 'decreased', 'reduced', 
                              'implemented', 'developed', 'created', 'led', 'managed', 'delivered']
        
        for pattern in resp_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                item = match.group(1).strip()
                if len(item) > 10:
                    # Check if it's an achievement
                    if any(keyword in item.lower() for keyword in achievement_keywords):
                        achievements.append(item)
                    else:
                        responsibilities.append(item)
        
        return responsibilities[:10], achievements[:10]  # Limit to top 10 each
    
    def _analyze_career_progression(self, job_titles: List[str]) -> Dict[str, any]:
        """
        Analyze career progression based on job titles.
        """
        progression = {
            'shows_growth': False,
            'leadership_progression': False,
            'technical_progression': False,
            'progression_score': 0
        }
        
        if len(job_titles) < 2:
            return progression
        
        # Check for seniority progression
        seniority_levels = ['intern', 'junior', 'associate', 'mid', 'senior', 'lead', 'principal', 'director', 'vp']
        title_levels = []
        
        for title in job_titles:
            title_lower = title.lower()
            for i, level in enumerate(seniority_levels):
                if level in title_lower:
                    title_levels.append(i)
                    break
            else:
                title_levels.append(3)  # Default to mid-level
        
        if len(title_levels) > 1:
            progression['shows_growth'] = max(title_levels) > min(title_levels)
            progression['progression_score'] = max(title_levels) - min(title_levels)
        
        # Check for leadership progression
        leadership_keywords = ['manager', 'director', 'lead', 'head', 'vp', 'chief']
        progression['leadership_progression'] = any(
            any(keyword in title.lower() for keyword in leadership_keywords)
            for title in job_titles
        )
        
        # Check for technical progression
        technical_keywords = ['engineer', 'developer', 'architect', 'specialist', 'analyst']
        progression['technical_progression'] = any(
            any(keyword in title.lower() for keyword in technical_keywords)
            for title in job_titles
        )
        
        return progression
    
    def analyze_education(self, text: str) -> Dict[str, any]:
        """
        Analyze educational background from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with education analysis
        """
        education_analysis = {
            'degrees': [],
            'institutions': [],
            'fields_of_study': [],
            'graduation_years': [],
            'gpa': None,
            'honors': [],
            'education_level': 'high_school'
        }
        
        doc = self.nlp(text)
        
        # Extract institutions using NER
        organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        # Filter for educational institutions
        edu_keywords = ['university', 'college', 'institute', 'school', 'academy']
        institutions = []
        for org in organizations:
            if any(keyword in org.lower() for keyword in edu_keywords):
                institutions.append(org)
        
        education_analysis['institutions'] = institutions
        
        # Extract degrees
        degree_patterns = [
            r'\b(?:Bachelor|Master|PhD|Doctorate|Associate|MBA|MS|BS|BA|MA|MSc|BSc)\b[^.]*',
            r'\b(?:B\.?A\.?|B\.?S\.?|M\.?A\.?|M\.?S\.?|Ph\.?D\.?|MBA)\b[^.]*'
        ]
        
        degrees = []
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                degree = match.group().strip()
                if len(degree) < 100:  # Reasonable length
                    degrees.append(degree)
        
        education_analysis['degrees'] = list(set(degrees))
        
        # Determine education level
        if any('phd' in degree.lower() or 'doctorate' in degree.lower() for degree in degrees):
            education_analysis['education_level'] = 'doctorate'
        elif any('master' in degree.lower() or 'mba' in degree.lower() for degree in degrees):
            education_analysis['education_level'] = 'masters'
        elif any('bachelor' in degree.lower() for degree in degrees):
            education_analysis['education_level'] = 'bachelors'
        elif any('associate' in degree.lower() for degree in degrees):
            education_analysis['education_level'] = 'associates'
        
        # Extract GPA
        gpa_match = re.search(r'gpa[:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
        if gpa_match:
            try:
                education_analysis['gpa'] = float(gpa_match.group(1))
            except ValueError:
                pass
        
        # Extract honors
        honor_patterns = [
            r'magna cum laude',
            r'summa cum laude',
            r'cum laude',
            r'dean\'s list',
            r'honor roll',
            r'valedictorian',
            r'salutatorian'
        ]
        
        honors = []
        for pattern in honor_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                honors.append(pattern.title())
        
        education_analysis['honors'] = honors
        
        return education_analysis
    
    def calculate_job_match_score(self, candidate_skills: List[str], job_requirements: List[str]) -> Dict[str, any]:
        """
        Calculate how well candidate skills match job requirements.
        
        Args:
            candidate_skills: List of candidate skills
            job_requirements: List of required skills for the job
            
        Returns:
            Dictionary with match analysis
        """
        if not job_requirements:
            return {'match_score': 0, 'matched_skills': [], 'missing_skills': job_requirements}
        
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        job_requirements_lower = [req.lower() for req in job_requirements]
        
        matched_skills = []
        missing_skills = []
        
        for req in job_requirements:
            req_lower = req.lower()
            if any(self._skills_match(req_lower, skill) for skill in candidate_skills_lower):
                matched_skills.append(req)
            else:
                missing_skills.append(req)
        
        match_score = (len(matched_skills) / len(job_requirements)) * 100 if job_requirements else 0
        
        return {
            'match_score': round(match_score, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'total_required': len(job_requirements),
            'total_matched': len(matched_skills)
        }
    
    def _skills_match(self, skill1: str, skill2: str) -> bool:
        """
        Check if two skills match (with some flexibility for similar technologies).
        """
        # Exact match
        if skill1 == skill2:
            return True
        
        # Partial match
        if skill1 in skill2 or skill2 in skill1:
            return True
        
        # Handle common variations
        variations = {
            'javascript': ['js', 'node.js', 'nodejs'],
            'typescript': ['ts'],
            'python': ['py'],
            'postgresql': ['postgres'],
            'mongodb': ['mongo'],
            'kubernetes': ['k8s'],
            'docker': ['containerization'],
            'aws': ['amazon web services'],
            'gcp': ['google cloud platform', 'google cloud']
        }
        
        for main_skill, variants in variations.items():
            if (skill1 == main_skill and skill2 in variants) or \
               (skill2 == main_skill and skill1 in variants):
                return True
        
        return False

