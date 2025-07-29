import PyPDF2
import pdfplumber
import re
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Advanced PDF processing service for resume analysis.
    Handles text extraction, structural analysis, and content categorization.
    """
    
    def __init__(self):
        self.section_patterns = {
            'contact': [
                r'contact\s+information',
                r'personal\s+details',
                r'contact\s+details'
            ],
            'summary': [
                r'professional\s+summary',
                r'career\s+summary',
                r'summary',
                r'profile',
                r'objective',
                r'career\s+objective'
            ],
            'experience': [
                r'work\s+experience',
                r'professional\s+experience',
                r'employment\s+history',
                r'career\s+history',
                r'experience'
            ],
            'education': [
                r'education',
                r'academic\s+background',
                r'educational\s+background',
                r'qualifications'
            ],
            'skills': [
                r'skills',
                r'technical\s+skills',
                r'core\s+competencies',
                r'competencies',
                r'expertise'
            ],
            'certifications': [
                r'certifications',
                r'certificates',
                r'professional\s+certifications',
                r'licenses'
            ],
            'projects': [
                r'projects',
                r'key\s+projects',
                r'notable\s+projects',
                r'project\s+experience'
            ]
        }
    
    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, bool]:
        """
        Extract text from PDF using multiple methods for maximum accuracy.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, success_flag)
        """
        try:
            # Method 1: Try pdfplumber first (better for complex layouts)
            text = self._extract_with_pdfplumber(file_path)
            if text and len(text.strip()) > 50:
                return text, True
            
            # Method 2: Fallback to PyPDF2
            text = self._extract_with_pypdf2(file_path)
            if text and len(text.strip()) > 50:
                return text, True
            
            logger.warning(f"Limited text extracted from {file_path}")
            return text or "", False
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return "", False
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber (preserves layout better)."""
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        return '\n'.join(text_content)
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2 (fallback method)."""
        text_content = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
        
        return '\n'.join(text_content)
    
    def analyze_document_structure(self, text: str) -> Dict[str, any]:
        """
        Analyze the structure of the resume document.
        
        Args:
            text: Extracted text from the resume
            
        Returns:
            Dictionary containing structural analysis
        """
        lines = text.split('\n')
        
        structure = {
            'total_lines': len(lines),
            'sections_found': [],
            'section_boundaries': {},
            'formatting_indicators': {
                'has_bullet_points': bool(re.search(r'[•·▪▫◦‣⁃]', text)),
                'has_numbered_lists': bool(re.search(r'^\s*\d+\.', text, re.MULTILINE)),
                'has_dates': bool(re.search(r'\b\d{4}\b|\b\d{1,2}/\d{4}\b|\b\w+\s+\d{4}\b', text)),
                'has_email': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
                'has_phone': bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\(\d{3}\)\s*\d{3}[-.]?\d{4}\b', text))
            }
        }
        
        # Identify sections
        for section_name, patterns in self.section_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                if matches:
                    structure['sections_found'].append(section_name)
                    structure['section_boundaries'][section_name] = [
                        match.start() for match in matches
                    ]
                    break
        
        return structure
    
    def extract_contact_information(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract contact information from resume text.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with contact information
        """
        contact_info = {
            'name': None,
            'email': None,
            'phone': None,
            'address': None,
            'linkedin': None,
            'github': None
        }
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone number
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',
            r'\+\d{1,3}\s*\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
                break
        
        # Extract LinkedIn profile
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        # Extract GitHub profile
        github_match = re.search(r'github\.com/[\w-]+', text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group()
        
        # Extract name (heuristic: first line that looks like a name)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line.split()) <= 4:
                # Check if it looks like a name (no numbers, reasonable length)
                if not re.search(r'\d', line) and 5 <= len(line) <= 50:
                    # Avoid common header words
                    avoid_words = ['resume', 'cv', 'curriculum', 'vitae', 'contact', 'information']
                    if not any(word in line.lower() for word in avoid_words):
                        contact_info['name'] = line
                        break
        
        return contact_info
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract content from different resume sections.
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary with section content
        """
        sections = {}
        structure = self.analyze_document_structure(text)
        
        # If no clear sections found, try to extract based on common patterns
        if not structure['sections_found']:
            return self._extract_sections_heuristic(text)
        
        # Extract sections based on identified boundaries
        text_length = len(text)
        section_positions = []
        
        for section_name, positions in structure['section_boundaries'].items():
            if positions:
                section_positions.append((positions[0], section_name))
        
        # Sort by position
        section_positions.sort()
        
        # Extract content between section boundaries
        for i, (start_pos, section_name) in enumerate(section_positions):
            if i + 1 < len(section_positions):
                end_pos = section_positions[i + 1][0]
            else:
                end_pos = text_length
            
            section_content = text[start_pos:end_pos].strip()
            sections[section_name] = section_content
        
        return sections
    
    def _extract_sections_heuristic(self, text: str) -> Dict[str, str]:
        """
        Extract sections using heuristic methods when clear boundaries aren't found.
        """
        sections = {}
        lines = text.split('\n')
        
        # Try to identify experience section by looking for date patterns
        experience_lines = []
        for i, line in enumerate(lines):
            if re.search(r'\b\d{4}\b.*\b\d{4}\b|\b\d{4}\b.*present', line, re.IGNORECASE):
                # Found a line with date range, likely experience
                start_idx = max(0, i - 2)
                end_idx = min(len(lines), i + 5)
                experience_lines.extend(lines[start_idx:end_idx])
        
        if experience_lines:
            sections['experience'] = '\n'.join(experience_lines)
        
        # Try to identify skills section by looking for technical terms
        skill_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 
                         'react', 'angular', 'vue', 'node', 'spring', 'django', 'flask']
        
        skills_lines = []
        for line in lines:
            if any(keyword in line.lower() for keyword in skill_keywords):
                skills_lines.append(line)
        
        if skills_lines:
            sections['skills'] = '\n'.join(skills_lines)
        
        return sections
    
    def validate_pdf_security(self, file_path: str) -> Dict[str, bool]:
        """
        Validate PDF security and integrity.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary with security validation results
        """
        validation = {
            'is_valid': False,
            'is_encrypted': False,
            'has_restrictions': False,
            'file_size_ok': False,
            'error_message': None
        }
        
        try:
            # Check file size (limit to 10MB)
            import os
            file_size = os.path.getsize(file_path)
            validation['file_size_ok'] = file_size <= 10 * 1024 * 1024
            
            # Check PDF structure
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                validation['is_encrypted'] = pdf_reader.is_encrypted
                validation['is_valid'] = True
                
                # Check for restrictions
                if hasattr(pdf_reader, 'metadata') and pdf_reader.metadata:
                    # PDF is readable
                    validation['has_restrictions'] = False
                
        except Exception as e:
            validation['error_message'] = str(e)
            logger.error(f"PDF validation failed for {file_path}: {str(e)}")
        
        return validation

