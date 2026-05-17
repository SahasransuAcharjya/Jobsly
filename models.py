from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    description: Optional[str] = None
    source: Optional[str] = None

    def to_dict(self):
        return asdict(self)
