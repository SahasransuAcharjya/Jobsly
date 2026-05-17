import logging
import time
import os
from bs4 import BeautifulSoup
from typing import List, Optional
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from src.models import Job
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class NaukriScraper(BaseScraper):
    """Scrape job listings from Naukri using undetected-chromedriver."""
    
    def __init__(self, url: str):
        super().__init__(url)
        self.delay = int(os.getenv("DELAY_BETWEEN_PAGES", "2"))
        
    def _setup_driver(self):
        logger.info("Setting up undetected-chromedriver...")
        options = uc.ChromeOptions()
        # Add headless option if desired
        # options.add_argument('--headless')
        driver = uc.Chrome(options=options)
        return driver

    def parse(self, html_content: str) -> List[Job]:
        jobs = []
        soup = BeautifulSoup(html_content, "html.parser")
        job_cards = soup.select(".srp-jobtuple-wrapper, #listContainer > div[class*='job-listing-container'] > div > div")
        
        for card in job_cards:
            title_elem = card.select_one("a.title")
            if not title_elem or not title_elem.get_text(strip=True):
                continue
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get("href")
            
            comp_elem = card.select_one("a.comp-name")
            company = comp_elem.get_text(strip=True) if comp_elem else None
            
            loc_elem = card.select_one(".locWdth")
            location = loc_elem.get_text(strip=True) if loc_elem else None
            
            jobs.append(Job(
                title=title,
                company=company,
                location=location,
                link=link,
                source="Naukri"
            ))
            
        return jobs

    def scrape(self) -> List[Job]:
        driver = self._setup_driver()
        all_jobs = []
        try:
            logger.info(f"Navigating to {self.url}")
            driver.get(self.url)
            
            # Wait for the page to load and JS to render
            time.sleep(self.delay + 3)
            
            html_content = driver.page_source
            jobs = self.parse(html_content)
            all_jobs.extend(jobs)
            
            # Here we could implement pagination logic to go to the next page
            # based on MAX_PAGES from env
            
        finally:
            driver.quit()
            
        return all_jobs
