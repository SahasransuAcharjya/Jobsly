import logging
import os
from dotenv import load_dotenv

from src.scrapers.naukri import NaukriScraper
from src.scrapers.linkedin import LinkedInScraper
from src.scrapers.wellfound import WellfoundScraper
from src.query_parser import parse_query
from src.csv_writer import write_jobs_to_csv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Job Agent...")
    
    # Configuration
    role = "python developer"
    location = "bangalore"
    source = "wellfound"
    
    logger.info(f"Searching for {role} jobs in {location} on {source}...")
    
    try:
        url = parse_query(role, location, source)
        logger.info(f"Target URL: {url}")
        
        # Initialize scraper based on source
        if source == "naukri":
            scraper = NaukriScraper(url)
        elif source == "linkedin":
            scraper = LinkedInScraper(url)
        elif source == "wellfound":
            scraper = WellfoundScraper(url)
        else:
            logger.error(f"Scraper for {source} not implemented yet.")
            return

        # Scrape jobs
        jobs = scraper.scrape()
        
        # Save results
        if jobs:
            logger.info(f"Found {len(jobs)} jobs. Saving to CSV...")
            write_jobs_to_csv(jobs)
        else:
            logger.info("No jobs found.")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
