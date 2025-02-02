from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.sql import func
from app.models import Parcela
from app.database.db import get_db
from app.schemas.schemas import Parcela as ParcelaSchema, ParcelaCreate, ParcelaUpdate
from geoalchemy2.shape import to_shape
from shapely import wkt
from shapely.errors import WKTReadingError
from typing import List, Optional
import json

router = APIRouter()

# Obtener todas las parcelas
@router.get("/parcelas", response_model=List[ParcelaSchema])
def get_parcelas(db: Session = Depends(get_db)):
        parcelas = (
            db.query(
                Parcela.id,
                Parcela.nombre,
                Parcela.cultivo,
                Parcela.area,
                func.ST_AsGeoJSON(Parcela.geom).label("geom")  # Convierte a GeoJSON
            ).all()
        )
        if not parcelas:
            raise HTTPException(status_code=404, detail="No parcelas found")

        return [{"id": p.id, "nombre": p.nombre, "geom": p.geom, "cultivo":p.cultivo} for p in parcelas]

# Obtener una parcela por ID
@router.get("/parcelas/{id}", response_model=ParcelaSchema)
def get_parcela(id: int, db: Session = Depends(get_db)):
        # Consulta con conversión a GeoJSON
        parcela = (
            db.query(
                Parcela.id,
                Parcela.nombre,
                Parcela.cultivo,
                Parcela.area,
                func.ST_AsGeoJSON(Parcela.geom).label("geom")
            )
            .filter(Parcela.id == id)
            .first()
        )
        
        if not parcela:
            raise HTTPException(status_code=404, detail="Parcela not found")
        
        # Devuelve los datos en formato dict
        return {"id": parcela.id, "nombre": parcela.nombre, "geom": parcela.geom, "cultivo": parcela.cultivo}

# Crear una nueva parcela
@router.post("/parcelas", response_model=ParcelaSchema)
def create_parcela(parcela: ParcelaCreate, db: Session = Depends(get_db)):
        nueva_parcela = Parcela(
            nombre=parcela.nombre or "Sin nombre",
            geom=func.ST_GeomFromGeoJSON(parcela.geom) if parcela.geom else "SRID=4326;POLYGON EMPTY",
            cultivo=parcela.cultivo
        )

        db.add(nueva_parcela)
        db.commit()
        db.refresh(nueva_parcela)

        # Consultar y devolver la parcela insertada
        parcela_resultado = db.query(
            Parcela.id,
            Parcela.nombre,
            func.ST_AsGeoJSON(Parcela.geom).label("geom"),
            Parcela.cultivo,
            Parcela.area
        ).filter(Parcela.id == nueva_parcela.id).first()

        return {
            "id": parcela_resultado.id,
            "nombre": parcela_resultado.nombre,
            "geom": parcela_resultado.geom,
            "cultivo": parcela_resultado.cultivo,
            "area": parcela_resultado.area
        }

# Actualizar una parcela
@router.put("/parcelas/{id}", response_model=ParcelaUpdate)
def update_parcela(id: int, parcela: ParcelaUpdate, db: Session = Depends(get_db)):
    db_parcela = db.query(Parcela).filter(Parcela.id == id).first()

    if not db_parcela:
        raise HTTPException(status_code=404, detail="Parcela no encontrada")
    for key, value in parcela.dict(exclude_unset=True).items():
        setattr(db_parcela, key, value)

    db.commit()
    db.refresh(db_parcela)
    
    # 🔥 Convertir geom a formato WKT (string)
    geom_wkt = to_shape(db_parcela.geom).wkt if db_parcela.geom else None

    response = JSONResponse(
        content={
            "nombre": db_parcela.nombre,
            "geom": geom_wkt,  # <-- Ahora geom es un string válido
            "cultivo": db_parcela.cultivo
        }
    )

    # 🔥 Forzar encabezado CORS en respuesta 🔥
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response

#Eliminar una parcela
@router.delete("/parcelas/{parcela_id}")
def delete_parcela(parcela_id: int, db: Session = Depends(get_db)):
    parcela_db = db.query(Parcela).filter(Parcela.id == parcela_id).first()
    if not parcela_db:
        raise HTTPException(status_code=404, detail="Parcela no encontrada")
    db.delete(parcela_db)
    db.commit()
    return {"message": "Parcela eliminada correctamente"}