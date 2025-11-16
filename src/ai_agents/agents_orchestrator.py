import asyncio
from typing import Dict, List
from celery import Celery
from ..config import settings
from .resume_agent import ResumeAgent
from .application_agent import ApplicationAgent
from .communication_agent import CommunicationAgent
from ..job_scraping.job_matcher import JobMatcher

celery_app = Celery('job_automator', broker=settings.REDIS_URL)

class AgentOrchestrator:
    def __init__(self):
        self.resume_agent = ResumeAgent()
        self.application_agent = ApplicationAgent()
        self.communication_agent = CommunicationAgent()
        self.job_matcher = JobMatcher()
    
    async def full_cycle_automation(self, user_id: str, preferences: Dict) -> Dict:
        """Execute full job application cycle for a user"""
        
        # 1. Process user documents
        user_profile = await self._process_user_documents(user_id)
        
        # 2. Scrape and match jobs
        matched_jobs = await self._find_matching_jobs(user_profile, preferences)
        
        # 3. Automated applications
        applications = await self._process_applications(user_id, user_profile, matched_jobs)
        
        # 4. Set up monitoring and follow-ups
        await self._setup_application_tracking(user_id, applications)
        
        return {
            "status": "success",
            "jobs_found": len(matched_jobs),
            "applications_submitted": len(applications),
            "next_steps": "Monitoring applications and scheduling follow-ups"
        }
    
    async def _process_user_documents(self, user_id: str) -> Dict:
        """Process and enhance user's resume and documents"""
        documents = await self.resume_agent.process_user_documents(user_id)
        enhanced_profile = await self.resume_agent.enhance_profile(documents)
        return enhanced_profile
    
    async def _find_matching_jobs(self, user_profile: Dict, preferences: Dict) -> List[Dict]:
        """Find and match jobs based on user profile and preferences"""
        all_jobs = await self.job_matcher.scrape_multiple_sources(
            keywords=preferences.get('keywords', []),
            locations=preferences.get('locations', []),
            industries=preferences.get('industries', [])
        )
        
        matched_jobs = self.job_matcher.calculate_matches(all_jobs, user_profile)
        return matched_jobs[:50]  # Limit to top 50 matches
    
    async def _process_applications(self, user_id: str, user_profile: Dict, jobs: List[Dict]) -> List[Dict]:
        """Process and submit job applications"""
        applications = []
        
        for job in jobs:
            if job['match_score'] >= 80:  # Only apply to high-match jobs
                try:
                    application_result = await self.application_agent.submit_application(
                        user_id, user_profile, job
                    )
                    applications.append(application_result)
                    
                    # Notify user
                    await self.communication_agent.send_application_confirmation(
                        user_id, job, application_result
                    )
                    
                    await asyncio.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error applying to {job['company']}: {e}")
                    continue
        
        return applications

@celery_app.task
def start_automation_cycle(user_id: str, preferences: Dict):
    """Celery task to start automation cycle"""
    orchestrator = AgentOrchestrator()
    return asyncio.run(orchestrator.full_cycle_automation(user_id, preferences))
