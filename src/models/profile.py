from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl

class PersonalInfo(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    location: str
    linkedin: Optional[HttpUrl]
    website: Optional[HttpUrl]
    github: Optional[HttpUrl]
    summary: str

class Education(BaseModel):
    degree: str
    field_of_study: str
    institution: str
    location: str
    start_date: str  # Format: YYYY-MM-DD or YYYY
    end_date: str    # Format: YYYY-MM-DD, YYYY, or 'present'
    gpa: Optional[str]

class WorkExperience(BaseModel):
    job_title: str
    company: str
    location: str
    start_date: str  # Format: YYYY-MM-DD or YYYY
    end_date: str    # Format: YYYY-MM-DD, YYYY, or 'present'
    description: List[str]
    link: Optional[HttpUrl]

class Project(BaseModel):
    name: str
    description: List[str]
    technologies: List[str]
    link: Optional[HttpUrl]
    start_date: str  # Format: YYYY-MM-DD or YYYY
    end_date: str    # Format: YYYY-MM-DD, YYYY, or 'present'

class Certification(BaseModel):
    name: str
    issuer: str
    date_earned: str  # Format: YYYY-MM-DD or YYYY

class Profile(BaseModel):
    personal_info: PersonalInfo
    education: List[Education]
    work_experience: List[WorkExperience]
    skills: List[str]
    projects: List[Project]
    certifications: List[Certification]
    languages: List[str]
