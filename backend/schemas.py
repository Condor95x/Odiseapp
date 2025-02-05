from pydantic import BaseModel, validator
from typing import Optional

class ParcelaBase(BaseModel):
    nombre: str
    cultivo: Optional[str]
    geom: str  # WKT (Well-Known Text)

    @validator("geom")
    def validate_geom(cls, geom):
      try:
        from geoalchemy2 import WKTElement
        WKTElement(geom, srid=4326) #Verifica que el WKT sea valido
        return geom
      except Exception as e:
        raise ValueError("Invalid WKT format")
class ParcelaCreate(ParcelaBase):
    pass

class ParcelaUpdate(BaseModel): #Schema para actualizar, campos opcionales
    nombre: Optional[str]
    cultivo: Optional[str]
    geom: Optional[str]

    @validator("geom")
    def validate_geom(cls, geom):
      if geom is None:
        return None
      try:
        from geoalchemy2 import WKTElement
        WKTElement(geom, srid=4326) #Verifica que el WKT sea valido
        return geom
      except Exception as e:
        raise ValueError("Invalid WKT format")

class Parcela(ParcelaBase):
    id: int

    class Config:
        from_attributes = True