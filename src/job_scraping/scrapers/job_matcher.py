from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.skill_weights = {
            'python': 1.2, 'java': 1.1, 'javascript': 1.1, 'react': 1.3,
            'node.js': 1.2, 'aws': 1.4, 'docker': 1.3, 'kubernetes': 1.4,
            'machine learning': 1.5, 'ai': 1.5, 'data science': 1.4,
            'project management': 1.2, 'agile': 1.1, 'scrum': 1.1
        }
    
    def calculate_match_scores(self, jobs: List[Dict], user_profile: Dict) -> List[Dict]:
        """Calculate match scores between jobs and user profile"""
        
        enhanced_jobs = []
        
        for job in jobs:
            match_score = self._calculate_individual_match(job, user_profile)
            job['match_score'] = match_score
            job['match_breakdown'] = self._get_match_breakdown(job, user_profile)
            enhanced_jobs.append(job)
        
        # Sort by match score
        return sorted(enhanced_jobs, key=lambda x: x['match_score'], reverse=True)
    
    def _calculate_individual_match(self, job: Dict, user_profile: Dict) -> float:
        """Calculate individual job match score"""
        
        total_score = 0
        weights = {
            'skills': 0.4,
            'experience': 0.2,
            'location': 0.15,
            'salary': 0.15,
            'education': 0.1
        }
        
        # Skills match
        skills_score = self._calculate_skills_match(job, user_profile)
        total_score += skills_score * weights['skills']
        
        # Experience match
        experience_score = self._calculate_experience_match(job, user_profile)
        total_score += experience_score * weights['experience']
        
        # Location match
        location_score = self._calculate_location_match(job, user_profile)
        total_score += location_score * weights['location']
        
        # Salary match
        salary_score = self._calculate_salary_match(job, user_profile)
        total_score += salary_score * weights['salary']
        
        # Education match
        education_score = self._calculate_education_match(job, user_profile)
        total_score += education_score * weights['education']
        
        return min(100, total_score * 100)
    
    def _calculate_skills_match(self, job: Dict, user_profile: Dict) -> float:
        """Calculate skills compatibility score"""
        
        job_skills = self._extract_skills_from_text(job.get('description', '') + ' ' + job.get('title', ''))
        user_skills = user_profile.get('skills', [])
        
        if not job_skills or not user_skills:
            return 0.5  # Neutral score if no skills data
        
        # Calculate weighted skill match
        matched_skills = set(job_skills) & set(user_skills)
        total_weight = sum(self.skill_weights.get(skill.lower(), 1.0) for skill in job_skills)
        matched_weight = sum(self.skill_weights.get(skill.lower(), 1.0) for skill in matched_skills)
        
        return matched_weight / total_weight if total_weight > 0 else 0
    
    def _calculate_experience_match(self, job: Dict, user_profile: Dict) -> float:
        """Calculate experience level match"""
        
        job_experience = self._parse_experience_requirement(job.get('description', ''))
        user_experience = user_profile.get('years_experience', 0)
        
        if job_experience == 0:  # No experience requirement specified
            return 0.8
        
        if user_experience >= job_experience:
            return 1.0
        elif user_experience >= job_experience * 0.7:  # Within 30% of requirement
            return 0.7
        else:
            return 0.3
    
    def _calculate_location_match(self, job: Dict, user_profile: Dict) -> float:
        """Calculate location compatibility"""
        
        job_location = job.get('location', '').lower()
        user_locations = [loc.lower() for loc in user_profile.get('preferred_locations', [])]
        
        if not job_location or not user_locations:
            return 0.6  # Neutral if no location data
        
        # Exact match
        if job_location in user_locations:
            return 1.0
        
        # Province match
        job_province = self._extract_province(job_location)
        user_provinces = [self._extract_province(loc) for loc in user_locations]
        
        if job_province in user_provinces:
            return 0.8
        
        # Remote work
        if 'remote' in job_location or 'work from home' in job.get('description', '').lower():
            return 0.9
        
        return 0.2  # Low score for incompatible locations
    
    def _calculate_salary_match(self, job: Dict, user_profile: Dict) -> float:
        """Calculate salary expectation match"""
        
        job_salary = self._parse_salary(job.get('salary', ''))
        user_expected = user_profile.get('expected_salary', 0)
        
        if job_salary == 0 or user_expected == 0:
            return 0.7  # Neutral if no salary data
        
        if job_salary >=
