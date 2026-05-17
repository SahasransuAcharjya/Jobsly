import logging
import time
import os
from bs4 import BeautifulSoup
from typing import List
import undetected_chromedriver as uc

from src.models import Job
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class WellfoundScraper(BaseScraper):
    """Scrape job listings from Wellfound using undetected-chromedriver."""
    
    def __init__(self, url: str):
        super().__init__(url)
        self.delay = int(os.getenv("DELAY_BETWEEN_PAGES", "2"))
        
    def _setup_driver(self):
        logger.info("Setting up undetected-chromedriver for Wellfound...")
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        return driver

    def parse(self, html_content: str) -> List[Job]:
        jobs = []
        soup = BeautifulSoup(html_content, "html.parser")
        
        # User provided selector for job cards
        # #main > div.styles_component__VRc0I.styles_white__Nexe6 > div > div > div > div.flex.flex-col.relative.w-full > div:nth-child(7)
        job_cards = soup.select("#main > div[class*='styles_component'] > div > div > div > div.flex.flex-col.relative.w-full > div")
        
        for card in job_cards:
            title_elem = card.select_one("a[class*='styles_roleLink']")
            if not title_elem:
                # Try generic approach if specific class doesn't match
                title_elem = card.select_one("a")
                if not title_elem:
                    continue
                
            title = title_elem.get_text(strip=True)
            link = title_elem.get("href")
            if link and not link.startswith("http"):
                link = "https://wellfound.com" + link
            
            comp_elem = card.select_one("h2")
            company = comp_elem.get_text(strip=True) if comp_elem else None
            
            # Wellfound location is usually in a span next to the tags
            loc_elem = card.select_one("span[class*='styles_location']")
            location = loc_elem.get_text(strip=True) if loc_elem else None
            
            jobs.append(Job(
                title=title,
                company=company,
                location=location,
                link=link or "",
                source="Wellfound"
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
