from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import os

app = FastAPI()

# Mount the static directory to serve HTML/CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/api/jobs")
def get_jobs():
    """Reads jobs from the results.csv file and returns them as JSON."""
    if not os.path.exists("results.csv"):
        return {"jobs": []}
    
    try:
        df = pd.read_csv("results.csv")
        # Replace NaNs with empty strings or None to be JSON compliant
        df = df.fillna("")
        jobs = df.to_dict(orient="records")
        return {"jobs": jobs}
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return {"jobs": []}

if __name__ == "__main__":
    import uvicorn
    # This block allows running with: python app.py
    uvicorn.run(app, host="127.0.0.1", port=8000)
