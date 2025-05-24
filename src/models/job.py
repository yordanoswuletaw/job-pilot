from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class Sitelink(BaseModel):
    title: str
    link: HttpUrl

class Job(BaseModel):
    title: str
    link: Optional[HttpUrl]
    description: str
    position: int
    date: Optional[str]
    rating: Optional[float]
    rating_count: Optional[int]
    sitelinks: Optional[List[Sitelink]]
    
