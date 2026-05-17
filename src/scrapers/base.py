from abc import ABC, abstractmethod
from typing import List, Any
from src.models import Job

class BaseScraper(ABC):
    def __init__(self, url: str):
        self.url = url
        
    @abstractmethod
    def scrape(self) -> List[Job]:
        """Main method to execute the scraping process."""
        pass
        
    @abstractmethod
    def parse(self, html_content: Any) -> List[Job]:
        """Parse the HTML content to extract job listings."""
        pass
