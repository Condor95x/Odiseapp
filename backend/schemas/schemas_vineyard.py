from pydantic import BaseModel

class VineyardBase(BaseModel):
    description : str = None
    value : str = None

class VineyardResponse(VineyardBase):
    vy_id : str
    
    class Config:
        from_attributes = True
