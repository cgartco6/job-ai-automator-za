import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from typing import List, Dict
from ..job_matcher import JobMatcher

class IndeedScraper:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.job_matcher = JobMatcher()
    
    async def scrape_jobs(self, keywords: str, location: str, max_pages: int = 5) -> List[Dict]:
        """Scrape jobs from Indeed based on keywords and location"""
        jobs = []
        driver = webdriver.Chrome(options=self.options)
        
        try:
            for page in range(max_pages):
                url = self._build_url(keywords, location, page)
                driver.get(url)
                
                # Wait for job listings to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                )
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards:
                    job_data = self._parse_job_card(card)
                    if job_data:
                        jobs.append(job_data)
                
                await asyncio.sleep(2)  # Be respectful to the server
            
        finally:
            driver.quit()
        
        return jobs
    
    def _build_url(self, keywords: str, location: str, page: int) -> str:
        """Build Indeed search URL"""
        base_url = "https://www.indeed.com/jobs"
        params = {
            'q': keywords.replace(' ', '+'),
            'l': location.replace(' ', '+'),
            'start': page * 10
        }
        return f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def _parse_job_card(self, card) -> Dict:
        """Parse individual job card data"""
        try:
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            
            if not all([title_elem, company_elem, location_elem]):
                return None
            
            job_data = {
                'title': title_elem.text.strip(),
                'company': company_elem.text.strip(),
                'location': location_elem.text.strip(),
                'source': 'indeed',
                'posted_date': self._extract_date(card),
                'job_url': self._extract_job_url(card),
                'salary': self._extract_salary(card)
            }
            
            return job_data
        except Exception as e:
            print(f"Error parsing job card: {e}")
            return None
