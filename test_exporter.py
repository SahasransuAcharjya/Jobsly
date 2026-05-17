from models import Job
from exporter import export_jobs_to_csv

def test_exporter():
    # Create some dummy jobs
    dummy_jobs = [
        Job(
            title="Software Engineer",
            company="Acme Corp",
            location="Remote",
            url="https://example.com/job1",
            description="Looking for a Python developer.",
            source="Test"
        ),
        Job(
            title="Data Scientist",
            company="Globex",
            location="New York, NY",
            url="https://example.com/job2",
            description="Machine learning and data analysis.",
            source="Test"
        )
    ]
    
    # Export them
    export_jobs_to_csv(dummy_jobs, "test_results.csv")
    print("Test finished.")

if __name__ == "__main__":
    test_exporter()
