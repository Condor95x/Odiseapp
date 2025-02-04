from pydantic import BaseModel, field_validator
from typing import Optional
import json

class ParcelaBase(BaseModel):
    nombre:Optional[str] = None
    geom: Optional[str] = None  # GeoJSON como cadena de texto
    cultivo: Optional[str] = None
    area: Optional[float] = None

class ParcelaCreate(ParcelaBase):
    pass
class Parcela(ParcelaBase):
    id: int
    geom: str  # GeoJSON como cadena de texto

class ParcelaUpdate(ParcelaBase):
    id:int
    nombre:Optional[str] = None
    geom: Optional[str] = None  # GeoJSON como cadena de texto
    cultivo: Optional[str] = None
    area: Optional[float] = None

class Config:
    orm_mode = True