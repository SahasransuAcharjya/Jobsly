import csv
import os
from typing import List
from .models import Job

def write_jobs_to_csv(jobs: List[Job], filename: str = "output/jobs.csv"):
    if not jobs:
        print("No jobs to write.")
        return

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].model_dump().keys())
        
        if not file_exists:
            writer.writeheader()
            
        for job in jobs:
            writer.writerow(job.model_dump())
            
    print(f"Successfully wrote {len(jobs)} jobs to {filename}")
