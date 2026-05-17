import pandas as pd
from typing import List
from models import Job
import os

def export_jobs_to_csv(jobs: List[Job], filename: str = "results.csv"):
    """
    Export a list of Job objects to a CSV file.
    Appends to the file if it exists, otherwise creates a new one.
    """
    if not jobs:
        print("No jobs to export.")
        return
        
    df = pd.DataFrame([job.to_dict() for job in jobs])
    
    # If file exists, append without writing headers again
    file_exists = os.path.isfile(filename)
    
    df.to_csv(filename, mode='a', header=not file_exists, index=False)
    print(f"Successfully exported {len(jobs)} jobs to {filename}")
