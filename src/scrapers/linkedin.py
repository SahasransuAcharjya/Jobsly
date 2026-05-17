import logging
import time
import os
from bs4 import BeautifulSoup
from typing import List
import undetected_chromedriver as uc

from src.models import Job
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseScraper):
    """Scrape job listings from LinkedIn using undetected-chromedriver."""
    
    def __init__(self, url: str):
        super().__init__(url)
        self.delay = int(os.getenv("DELAY_BETWEEN_PAGES", "2"))
        
    def _setup_driver(self):
        logger.info("Setting up undetected-chromedriver for LinkedIn...")
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        return driver

    def parse(self, html_content: str) -> List[Job]:
        jobs = []
        soup = BeautifulSoup(html_content, "html.parser")
        
        # User provided selector for job cards
        # #main-content > section > ul > li:nth-child(2) > div
        job_cards = soup.select("#main-content > section > ul > li > div")
        
        for card in job_cards:
            # LinkedIn specific classes might vary, using generic links and texts
            link_elem = card.select_one("a.base-card__full-link, a")
            if not link_elem:
                continue
                
            title = link_elem.get_text(strip=True)
            link = link_elem.get("href", "").split("?")[0] # clean up tracking params
            
            comp_elem = card.select_one("h4.base-search-card__subtitle, .hidden-nested-link")
            company = comp_elem.get_text(strip=True) if comp_elem else None
            
            loc_elem = card.select_one("span.job-search-card__location")
            location = loc_elem.get_text(strip=True) if loc_elem else None
            
            jobs.append(Job(
                title=title,
                company=company,
                location=location,
                link=link,
                source="LinkedIn"
            ))
            
        return jobs

    def scrape(self) -> List[Job]:
        driver = self._setup_driver()
        all_jobs = []
        try:
            logger.info(f"Navigating to {self.url}")
            driver.get(self.url)
            
            time.sleep(self.delay + 3)
            
            html_content = driver.page_source
            jobs = self.parse(html_content)
            all_jobs.extend(jobs)
            
        finally:
            try:
                driver.quit()
            except OSError:
                pass # Ignore Windows Handle invalid error on quit
            
        return all_jobs
