from pydantic import BaseModel, validator, Field
from typing import Optional, Dict, Any
from datetime import date
from enum import Enum

class ConductionType(str, Enum):
    ESPALDERA = "ESPALDERA"
    VASO = "VASO"
    PARRAL = "PARRAL"
    LIRA = "LIRA"
    GUYOT = "GUYOT"

class ManagementType(str, Enum):
    CONVENTIONAL = "CONVENTIONAL"
    ORGANIC = "ORGANIC"
    BIODYNAMIC = "BIODYNAMIC"
    INTEGRATED = "INTEGRATED"

class PlotBase(BaseModel):
    plot_name: str = Field(..., description="Nombre de la parcela")
    plot_var: str = Field(..., description="Variedad de la vid")
    plot_rootstock: Optional[str] = Field(None, description="Portainjerto") 
    plot_implant_year: Optional[int] = Field(None, description="Año de implantación")
    plot_creation_year: Optional[int] = Field(None, description="Año de creación")
    plot_conduction: Optional[ConductionType] = Field(None, description="Sistema de conducción")
    plot_management: Optional[ManagementType] = Field(None, description="Tipo de manejo")
    plot_description: Optional[str] = Field(None, description="Descripción de la parcela")
    active: bool = Field(True, description="Estado activo de la parcela")      
    plot_geom: str = Field(..., description="Geometría en formato GeoJSON") # Modificado a GeoJSON
    plot_area: Optional[float] = Field(None, description="Área de la parcela en metros cuadrados")

    @validator("plot_implant_year", "plot_creation_year")
    def validate_years(cls, value):
        if value is not None:
            current_year = date.today().year
            if value < 1800 or value > current_year:
                raise ValueError(f"El año debe estar entre 1800 y {current_year}")
        return value
    
class PlotCreate(PlotBase):
    pass

class PlotUpdate(BaseModel):
    plot_name: Optional[str] = None
    plot_var: Optional[str] = None
    plot_rootstock: Optional[str] = None
    plot_implant_year: Optional[int] = None
    plot_creation_year: Optional[int] = None
    plot_conduction: Optional[ConductionType] = None
    plot_management: Optional[ManagementType] = None
    plot_description: Optional[str] = None
    active: Optional[bool] = None      
    plot_geom: Optional[str] = None
    plot_area: Optional[float] = None

    @validator("plot_geom")
    def validate_plot_geom(cls, value):
        if value is None:
            return None
        try:
            from geoalchemy2 import WKTElement
            WKTElement(value, srid=4326)
            return value
        except Exception as e:
            raise ValueError("Formato WKT inválido")

    @validator("plot_implant_year", "plot_creation_year")
    def validate_years(cls, value):
        if value is not None:
            current_year = date.today().year
            if value < 1800 or value > current_year:
                raise ValueError(f"El año debe estar entre 1800 y {current_year}")
        return value

class PlotResponse(BaseModel): 
    plot_id: int = Field(..., description="ID único de la parcela")
    plot_name: str = Field(..., description="Nombre de la parcela")
    plot_var: Optional[str] = Field(..., description="Variedad de la vid")
    plot_rootstock: Optional[str] = Field(None, description="Portainjerto")
    plot_implant_year: Optional[int] = Field(None, description="Año de implantación")
    plot_creation_year: Optional[int] = Field(None, description="Año de creación")
    plot_conduction: Optional[ConductionType] = Field(None, description="Sistema de conducción")
    plot_management: Optional[ManagementType] = Field(None, description="Tipo de manejo")
    plot_description: Optional[str] = Field(None, description="Descripción de la parcela")
    active: bool = Field(True, description="Estado activo de la parcela")
    plot_geom: Optional[str] = Field(None, description="Geometría en formato WKT")
    plot_area: float = Field(..., description="Área de la parcela en metros cuadrados")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "plot_id": 1,
                "plot_name": "Parcela Norte",
                "plot_var": "Tempranillo",
                "plot_rootstock": "110R",
                "plot_implant_year": 2015,
                "plot_creation_year": 2014,
                "plot_conduction": "espaldera",
                "plot_management": "orgánico",
                "plot_description": "Parce la principal de Tempranillo",
                "active": True,
                "plot_area": 10000.50
            }
        }


    #plot_var_details: Optional[GrapevineResponse] = None
    #plot_rootstock_details: Optional[GrapevineResponse] = None

    class Config:
        from_attributes = True