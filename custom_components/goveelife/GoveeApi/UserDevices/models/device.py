# models/device.py

from typing import List
from pydantic import BaseModel
from .capability import Capability

class Device(BaseModel):
    sku: str
    device: str
    deviceName: str
    type: str
    capabilities: List[Capability]
