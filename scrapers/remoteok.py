import requests
from typing import List
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Job

load_dotenv()

class RemoteOKScraper:
    def __init__(self):
        self.base_url = "https://remoteok.com/api"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        
        proxy_url = os.getenv("PROXY_URL")
        self.proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    def fetch_jobs(self, job_title: str) -> List[Job]:
        """
        Fetches jobs from RemoteOK API based on a job title/tag.
        """
        print(f"Fetching RemoteOK jobs for: '{job_title}'...")
        jobs = []
        try:
            # We can use the job_title as a tag. We might want to replace spaces with hyphens or just pass it as is.
            tag = job_title.lower().replace(" ", "-")
            response = requests.get(f"{self.base_url}?tags={tag}", headers=self.headers, proxies=self.proxies, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # The first item in RemoteOK API response is usually legal/metadata, skip it if it's not a job
            for item in data:
                if 'legal' in item:
                    continue
                    
                # Map to our standard model
                job = Job(
                    title=item.get("position", "Unknown Title"),
                    company=item.get("company", "Unknown Company"),
                    location=item.get("location", "Remote"),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    source="RemoteOK"
                )
                jobs.append(job)
                
            print(f"Found {len(jobs)} jobs from RemoteOK.")
            
        except Exception as e:
            print(f"Error fetching from RemoteOK: {e}")
            
        return jobs

if __name__ == "__main__":
    scraper = RemoteOKScraper()
    found_jobs = scraper.fetch_jobs("python")
    for j in found_jobs[:2]:
        print(j.title, "-", j.company)
