# models/capability.py

from pydantic import BaseModel

class Capability(BaseModel):
    type: str
    instance: str
