import time
from bs4 import BeautifulSoup
from typing import List
import sys
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Job

load_dotenv()

class NaukriScraper:
    def __init__(self):
        self.proxy_url = os.getenv("PROXY_URL")
        
    def fetch_jobs(self, job_title: str) -> List[Job]:
        print(f"Fetching Naukri jobs for: '{job_title}' using Playwright...")
        jobs = []
        
        formatted_title = job_title.lower().replace(" ", "-")
        url = f"https://www.naukri.com/{formatted_title}-jobs"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Scroll slightly or wait for job cards to load if they are rendered dynamically
                try:
                    page.wait_for_selector(".srp-jobtuple-wrapper", timeout=10000)
                except Exception:
                    print("Could not find job tuples immediately, grabbing what is there.")
                
                html_content = page.content()
                browser.close()
                
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Select job cards using the identified selectors
            job_cards = soup.select(".srp-jobtuple-wrapper, .jobTuple")
            
            for card in job_cards:
                title_elem = card.select_one("a.title")
                if not title_elem or not title_elem.get_text(strip=True):
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get("href", "")
                
                comp_elem = card.select_one("a.comp-name")
                company = comp_elem.get_text(strip=True) if comp_elem else "Unknown Company"
                
                loc_elem = card.select_one(".locWdth")
                location = loc_elem.get_text(strip=True) if loc_elem else "Unknown Location"
                
                desc_elem = card.select_one(".job-desc")
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                job = Job(
                    title=title,
                    company=company,
                    location=location,
                    url=link,
                    description=description,
                    source="Naukri"
                )
                jobs.append(job)
                
            print(f"Found {len(jobs)} jobs from Naukri.")
            
        except Exception as e:
            print(f"Error fetching from Naukri: {e}")
            
        return jobs

if __name__ == "__main__":
    scraper = NaukriScraper()
    found_jobs = scraper.fetch_jobs("python developer")
    for j in found_jobs[:2]:
        print(f"{j.title} - {j.company} ({j.location})")

if __name__ == "__main__":
    scraper = NaukriScraper()
    found_jobs = scraper.fetch_jobs("python developer")
    for j in found_jobs[:2]:
        print(f"{j.title} - {j.company} ({j.location})")
