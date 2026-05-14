
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WearableSyncStatusBase(BaseModel):
    provider: str
    status: str
    last_sync: Optional[datetime] = None

class WearableSyncStatusCreate(WearableSyncStatusBase):
    pass

class WearableSyncStatus(WearableSyncStatusBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True
