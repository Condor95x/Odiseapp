from pydantic import BaseModel, field_validator
from typing import Optional
import json

class ParcelaBase(BaseModel):
    nombre:Optional[str] = None
    geom: Optional[str] = None  # GeoJSON como cadena de texto
    cultivo: Optional[str] = None
    area: Optional[float] = None

class ParcelaCreate(ParcelaBase):
    @field_validator("geom", mode='before')
    def validar_geom(cls, valor):
        if valor:
            try:
                # Validar si el GeoJSON es correcto
                geometria_json = json.loads(valor)  # Intentar cargar como JSON
                if isinstance(geometria_json, dict) and "type" in geometria_json:
                    return valor  # Si es un GeoJSON válido, lo retornamos
            except ValueError:
                raise ValueError("El formato de la geometría GeoJSON es inválido.")
        return valor  # Si no se pasa ninguna geometría, retornamos None

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