from typing import List, Any
import logging
from src.models import Job
from src.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)

class RemoteOKScraper(BaseScraper):
    """Scrape job listings from RemoteOK."""
    
    def parse(self, html_content: Any) -> List[Job]:
        # TODO: Implement parsing logic for RemoteOK
        logger.warning("RemoteOK parsing not implemented yet")
        return []

    def scrape(self) -> List[Job]:
        # TODO: Implement fetching logic for RemoteOK
        logger.warning("RemoteOK scraping not implemented yet")
        return []
