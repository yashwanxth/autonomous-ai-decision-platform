from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    event_id: str
    entity_id: str
    event_type: str
    value: float
    timestamp: datetime
