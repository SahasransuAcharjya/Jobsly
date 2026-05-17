import requests
from bs4 import BeautifulSoup
from typing import List
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Job

class NaukriScraper:
    def __init__(self):
        # We need realistic headers to avoid getting blocked by basic anti-bot systems
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
    def fetch_jobs(self, job_title: str) -> List[Job]:
        print(f"Fetching Naukri jobs for: '{job_title}'...")
        jobs = []
        
        # Naukri's URL structure usually looks like: https://www.naukri.com/job-title-jobs
        # We'll format the title by replacing spaces with hyphens
        formatted_title = job_title.lower().replace(" ", "-")
        url = f"https://www.naukri.com/{formatted_title}-jobs"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Select job cards using the identified selectors
            job_cards = soup.select(".srp-jobtuple-wrapper, #listContainer > div[class*='job-listing-container'] > div > div")
            
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
                
                # Try to extract a brief description if present (often in a span/div with 'job-desc' class)
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
