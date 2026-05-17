import schedule
import time
import subprocess
import datetime
import sys

def job():
    print(f"[{datetime.datetime.now()}] Running scheduled Job Agent scraping...")
    # Change the job title and output file as needed
    subprocess.run([sys.executable, "main.py", "python developer", "--output", "results.csv"])
    print(f"[{datetime.datetime.now()}] Scheduled scraping completed.")

# Schedule the job to run every 12 hours
schedule.every(12).hours.do(job)

if __name__ == "__main__":
    print("Job Agent Scheduler started. Scraping every 12 hours.")
    print("Press Ctrl+C to exit.")
    
    # Run immediately on startup
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait one minute
