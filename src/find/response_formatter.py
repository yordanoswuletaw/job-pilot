from typing import List
from models.job import Job, Sitelink

def format_response(response) -> List[Job]:
    jobs: List[Job] = []
    for role in response[0]['organic']:
        
        job = Job(
            title=role['title'],
            link=role['link'],
            description=role['snippet'],
            position=role['position'],
            rating=role.get('rating', None),
            rating_count=role.get('rating_count', None),
            date=role.get('date', None),
            sitelinks=[Sitelink(title=sitelink['title'], link=sitelink['link']) for sitelink in role.get('sitelinks', [])]
        )
        jobs.append(job)
    return jobs
        