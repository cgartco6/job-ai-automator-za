import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import re

class SouthAfricaJobScrapers:
    def __init__(self):
        self.agencies = [
            {
                "name": "CareerJunction",
                "url": "https://www.careerjunction.co.za/jobs",
                "parser": self.parse_careerjunction
            },
            {
                "name": "PNet",
                "url": "https://www.pnet.co.za/jobs",
                "parser": self.parse_pnet
            },
            {
                "name": "IndeedZA",
                "url": "https://www.indeed.co.za/jobs",
                "parser": self.parse_indeed_za
            },
            {
                "name": "CareerBox",
                "url": "https://www.careerbox.co.za/jobs",
                "parser": self.parse_careerbox
            },
            {
                "name": "JobMail",
                "url": "https://www.jobmail.co.za/jobs",
                "parser": self.parse_jobmail
            },
            {
                "name": "Jobs4All",
                "url": "https://www.jobs4all.co.za/jobs",
                "parser": self.parse_jobs4all
            }
        ]
    
    async def scrape_all_agencies(self, keywords: List[str], locations: List[str]) -> List[Dict]:
        """Scrape jobs from all South African agencies"""
        all_jobs = []
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for agency in self.agencies:
                for keyword in keywords:
                    for location in locations:
                        task = self.scrape_agency(session, agency, keyword, location)
                        tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_jobs.extend(result)
        
        return all_jobs
    
    async def scrape_agency(self, session, agency: Dict, keyword: str, location: str) -> List[Dict]:
        """Scrape individual agency"""
        try:
            url = f"{agency['url']}?q={keyword}&l={location}"
            async with session.get(url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                return agency['parser'](soup, keyword, location)
        except Exception as e:
            print(f"Error scraping {agency['name']}: {e}")
            return []
    
    def parse_careerjunction(self, soup: BeautifulSoup, keyword: str, location: str) -> List[Dict]:
        """Parse CareerJunction job listings"""
        jobs = []
        job_cards = soup.find_all('div', class_='job-item')  # Update with actual class
        
        for card in job_cards:
            try:
                job = {
                    'title': self._safe_extract(card, '.job-title'),
                    'company': self._safe_extract(card, '.company-name'),
                    'location': location,
                    'salary': self._safe_extract(card, '.salary'),
                    'date_posted': self._safe_extract(card, '.date-posted'),
                    'description': self._safe_extract(card, '.job-description'),
                    'source': 'CareerJunction',
                    'url': self._extract_url(card),
                    'province': self._determine_province(location)
                }
                jobs.append(job)
            except Exception as e:
                continue
        
        return jobs
    
    def parse_pnet(self, soup: BeautifulSoup, keyword: str, location: str) -> List[Dict]:
        """Parse PNet job listings"""
        jobs = []
        # Similar implementation for PNet
        return jobs

    def parse_indeed_za(self, soup: BeautifulSoup, keyword: str, location: str) -> List[Dict]:
        """Parse Indeed South Africa job listings"""
        jobs = []
        # Implementation for Indeed South Africa
        return jobs
