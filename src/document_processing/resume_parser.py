import pdfplumber
import docx
import re
from typing import Dict, List, Any
import io

class ResumeParser:
    def __init__(self):
        self.section_keywords = {
            'experience': ['experience', 'employment', 'work history', 'career'],
            'education': ['education', 'qualifications', 'academic', 'degrees'],
            'skills': ['skills', 'competencies', 'technologies', 'programming'],
            'projects': ['projects', 'portfolio', 'achievements'],
            'certifications': ['certifications', 'licenses', 'certificates'],
            'personal': ['personal', 'about', 'profile', 'summary']
        }
    
    def parse_resume(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Parse resume file and extract structured information"""
        
        text = self._extract_text(file_content, filename)
        structured_data = self._structure_data(text)
        
        return {
            'raw_text': text,
            'structured': structured_data,
            'metadata': self._extract_metadata(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text)
        }
    
    def _extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract text from different file formats"""
        
        if filename.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_content)
        elif filename.lower().endswith(('.doc', '.docx')):
            return self._extract_from_docx(file_content)
        elif filename.lower().endswith('.txt'):
            return file_content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file format: {filename}")
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
    
    def _structure_data(self, text: str) -> Dict[str, str]:
        """Structure the resume text into sections"""
        lines = text.split('\n')
        structured = {}
        current_section = 'header'
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue
                
            section = self._identify_section(line_clean)
            if section:
                current_section = section
                structured[current_section] = []
            else:
                if current_section not in structured:
                    structured[current_section] = []
                structured[current_section].append(line_clean)
        
        # Convert lists to strings
        for section in structured:
            structured[section] = '\n'.join(structured[section])
            
        return structured
    
    def _identify_section(self, line: str) -> str:
        """Identify if a line is a section header"""
        line_lower = line.lower()
        for section, keywords in self.section_keywords.items():
            if any(keyword in line_lower for keyword in keywords):
                return section
        return None
    
    def _extract_metadata(self, text: str) -> Dict[str, str]:
        """Extract metadata like name, email, phone"""
        # Email regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Phone regex for South Africa
        phone_pattern = r'(\+27|0)[\s-]?[1-9][\s-]?[0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{4}'
        phones = re.findall(phone_pattern, text)
        
        return {
            'email': emails[0] if emails else '',
            'phone': phones[0] if phones else '',
            'name': self._extract_name(text)
        }
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name from resume"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line_clean = line.strip()
            if line_clean and not any(keyword in line_clean.lower() for keyword in ['cv', 'resume', 'curriculum']):
                # Simple heuristic: first substantial line that's not a header
                return line_clean
        return "Unknown"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mongodb', 'postgresql', 'aws', 'azure', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data analysis', 'project management',
            'agile', 'scrum', 'leadership', 'communication', 'problem solving'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
                
        return found_skills
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        # This is a simplified version - would use more sophisticated NLP in production
        experience = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['experience', 'employment']):
                # Look for experience entries in following lines
                for j in range(i+1, min(i+20, len(lines))):
                    exp_line = lines[j].strip()
                    if exp_line and len(exp_line) > 10:
                        experience.append({'raw': exp_line})
                        if len(experience) >= 5:  # Limit to 5 most recent
                            break
                break
                
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['education', 'qualification', 'degree']):
                for j in range(i+1, min(i+10, len(lines))):
                    edu_line = lines[j].strip()
                    if edu_line and len(edu_line) > 5:
                        education.append({'raw': edu_line})
                        if len(education) >= 3:
                            break
                break
                
        return education
