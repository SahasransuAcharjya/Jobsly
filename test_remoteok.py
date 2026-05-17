import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.remoteok import RemoteOKScraper
from exporter import export_jobs_to_csv

def test_remoteok_export():
    scraper = RemoteOKScraper()
    jobs = scraper.fetch_jobs("python")
    export_jobs_to_csv(jobs, "remoteok_results.csv")

if __name__ == "__main__":
    test_remoteok_export()
