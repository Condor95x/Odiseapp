from pydantic import BaseModel
from typing import Optional

class ParcelaBase(BaseModel):
    nombre: str
    geom: str  # WKT (Well-Known Text)
    cultivo: Optional[str]
    #area: Optional[float]

class ParcelaCreate(ParcelaBase):
    pass

class Parcela(ParcelaBase):
    id: int

    class Config:
        from_attributes = True