# models/response.py

from typing import List
from pydantic import BaseModel
from .device import Device

class Response(BaseModel):
    code: int
    message: str
    data: List[Device]
