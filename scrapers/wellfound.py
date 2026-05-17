import os
import sys
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from firecrawl import FirecrawlApp

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Job

# Load environment variables
load_dotenv()

# Define the extraction schema using Pydantic for Firecrawl LLM extraction
class JobExtraction(BaseModel):
    title: str = Field(description="The job title")
    company: str = Field(description="The name of the company hiring")
    location: str = Field(description="The location of the job, or 'Remote'")
    url: str = Field(description="The URL to the job posting")
    description: str = Field(description="A brief description of the role, if available", default="")

class ExtractSchema(BaseModel):
    jobs: List[JobExtraction]

class WellfoundScraper:
    def __init__(self):
        # The FirecrawlApp will automatically look for FIRECRAWL_API_KEY in the environment
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            print("Warning: FIRECRAWL_API_KEY not found in environment variables.")
        self.app = FirecrawlApp(api_key=api_key) if api_key else None
        
    def fetch_jobs(self, job_title: str) -> List[Job]:
        print(f"Fetching Wellfound jobs for: '{job_title}' using Firecrawl...")
        jobs = []
        
        if not self.app:
            print("Error: Firecrawl API key is missing. Cannot fetch from Wellfound.")
            return jobs
            
        # Wellfound's job search URL format
        formatted_title = job_title.lower().replace(" ", "-")
        url = f"https://wellfound.com/role/{formatted_title}"
        
        try:
            # Use Firecrawl's extract endpoint
            response = self.app.scrape_url(
                url, 
                params={
                    'formats': ['extract'],
                    'extract': {
                        'schema': ExtractSchema.model_json_schema()
                    }
                }
            )
            
            # The response contains the extracted data matching our schema
            extracted_data = response.get('extract', {})
            extracted_jobs = extracted_data.get('jobs', [])
            
            for item in extracted_jobs:
                job = Job(
                    title=item.get("title", "Unknown Title"),
                    company=item.get("company", "Unknown Company"),
                    location=item.get("location", "Remote"),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    source="Wellfound"
                )
                jobs.append(job)
                
            print(f"Found {len(jobs)} jobs from Wellfound.")
            
        except Exception as e:
            print(f"Error fetching from Wellfound: {e}")
            
        return jobs

if __name__ == "__main__":
    scraper = WellfoundScraper()
    found_jobs = scraper.fetch_jobs("python developer")
    for j in found_jobs[:2]:
        print(f"{j.title} - {j.company} ({j.location})")
