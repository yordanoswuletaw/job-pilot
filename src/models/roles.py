from typing import List
from pydantic import BaseModel

class Role(BaseModel):
    name: str
    description: str

class Roles(BaseModel):
    roles: List[Role]
    