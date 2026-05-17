import argparse
from scrapers.remoteok import RemoteOKScraper
from scrapers.naukri import NaukriScraper
from scrapers.wellfound import WellfoundScraper
from exporter import export_jobs_to_csv

def main():
    parser = argparse.ArgumentParser(description="Job Agent: Scrape job listings across multiple platforms.")
    parser.add_argument("title", type=str, help="The job title to search for (e.g., 'python developer')")
    parser.add_argument("--output", type=str, default="results.csv", help="The output CSV filename")
    
    args = parser.parse_args()
    job_title = args.title
    output_file = args.output
    
    all_jobs = []
    
    print("="*50)
    print(f"Starting Job Agent for: '{job_title}'")
    print("="*50)
    
    # Initialize scrapers
    remoteok = RemoteOKScraper()
    naukri = NaukriScraper()
    wellfound = WellfoundScraper()
    
    # 1. Scrape RemoteOK
    remoteok_jobs = remoteok.fetch_jobs(job_title)
    all_jobs.extend(remoteok_jobs)
    
    # 2. Scrape Naukri
    naukri_jobs = naukri.fetch_jobs(job_title)
    all_jobs.extend(naukri_jobs)
    
    # 3. Scrape Wellfound
    wellfound_jobs = wellfound.fetch_jobs(job_title)
    all_jobs.extend(wellfound_jobs)
    
    print("="*50)
    print(f"Total Jobs Found: {len(all_jobs)}")
    print("="*50)
    
    if all_jobs:
        export_jobs_to_csv(all_jobs, output_file)
    else:
        print("No jobs found to export.")

if __name__ == "__main__":
    main()
