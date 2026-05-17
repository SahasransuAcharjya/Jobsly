from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    link: str
    description: Optional[str] = None
    source: str
