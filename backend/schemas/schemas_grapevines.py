from pydantic import BaseModel
from typing import Optional

class GrapevineBase(BaseModel):
    gv_use: Optional[str] = None
    name: str
    synonyms: Optional[str] = None
    color: Optional[str] = None
    gv_type: Optional[str] = None
    maintenance_entity: Optional[str] = None

class GrapevineResponse(GrapevineBase):
    gv_id: str
    
    class Config:
        from_attributes = True
