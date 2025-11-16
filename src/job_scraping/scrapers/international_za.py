import asyncio
from typing import List, Dict
import aiohttp

class InternationalJobScraper:
    def __init__(self):
        self.international_sites = [
            {
                "name": "RemoteOK",
                "url": "https://remoteok.io/remote-jobs",
                "filters": {"allow_remote": True, "countries": ["worldwide"]}
            },
            {
                "name": "WeWorkRemotely",
                "url": "https://weworkremotely.com/categories/remote-programming-jobs",
                "filters": {"allow_remote": True}
            },
            {
                "name": "LinkedIn International",
                "url": "https://www.linkedin.com/jobs/search",
                "filters": {"remote": True, "location": "worldwide"}
            },
            {
                "name": "AngelList",
                "url": "https://angel.co/jobs",
                "filters": {"remote": True}
            }
        ]
    
    async def scrape_international_jobs(self, skills: List[str], remote_only: bool = True) -> List[Dict]:
        """Scrape international jobs suitable for South Africans"""
        all_jobs = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for site in self.international_sites:
                for skill in skills:
                    task = self.scrape_site(session, site, skill, remote_only)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_jobs.extend(result)
        
        # Filter jobs that are suitable for South Africans
        suitable_jobs = self._filter_for_south_africans(all_jobs)
        return suitable_jobs
    
    def _filter_for_south_africans(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs that are suitable for South African applicants"""
        filtered_jobs = []
        
        for job in jobs:
            # Check timezone compatibility
            if self._is_timezone_compatible(job):
                # Check for visa requirements
                if not self._requires_visa_sponsorship(job):
                    # Check for remote work capability
                    if self._can_work_remotely(job):
                        filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _is_timezone_compatible(self, job: Dict) -> bool:
        """Check if job timezone is compatible with South Africa (UTC+2)"""
        # Most European and some US companies can work with SA timezone
        preferred_timezones = ["UTC", "UTC+1", "UTC+2", "UTC+3", "GMT", "CET", "EET"]
        job_timezone = job.get('timezone', '').upper()
        
        if any(tz in job_timezone for tz in preferred_timezones):
            return True
        
        # Remote jobs with flexible hours are always compatible
        if job.get('flexible_hours', False):
            return True
            
        return False
    
    def _requires_visa_sponsorship(self, job: Dict) -> bool:
        """Check if job requires visa sponsorship (South Africans often need visas)"""
        description = job.get('description', '').lower()
        visa_keywords = ['visa sponsorship', 'relocation required', 'must relocate', 'us citizenship required']
        
        return any(keyword in description for keyword in visa_keywords)
    
    def _can_work_remotely(self, job: Dict) -> bool:
        """Check if job can be done remotely from South Africa"""
        return job.get('remote', False) or job.get('work_from_home', False)
