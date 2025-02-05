from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Parcela, ParcelaCreate, ParcelaUpdate
from crud import create_parcela, get_parcelas, get_parcela, update_parcela, delete_parcela
from geoalchemy2.shape import to_shape #Importa solo to_shape

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_parcela(parcela: ParcelaCreate, db: AsyncSession = Depends(get_db)):
    return await create_parcela(db, parcela)

@router.get("/")
async def read_parcelas(db: AsyncSession = Depends(get_db)):
    return await get_parcelas(db)

@router.get("/{parcela_id}", response_model=Parcela)
async def read_parcela(parcela_id: int, db: AsyncSession = Depends(get_db)):
    parcela_db = await get_parcela(db, parcela_id)
    if parcela_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcela not found")

    parcela_wkt = to_shape(parcela_db.geom).wkt if parcela_db.geom else None #Manejo de None
    parcela_schema = Parcela.model_validate({
            "id": parcela_db.id,
            "nombre": parcela_db.nombre,
            "cultivo": parcela_db.cultivo,
            "geom": parcela_wkt,
            "area": parcela_db.area
        })
    return parcela_schema

@router.put("/{parcela_id}", status_code=status.HTTP_200_OK)
async def update_parcela_endpoint(parcela_id: int, parcela: ParcelaUpdate, db: AsyncSession = Depends(get_db)):
    updated_parcela = await update_parcela(db, parcela_id, parcela)
    if updated_parcela is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcela not found")

    parcela_wkt = to_shape(updated_parcela.geom).wkt if updated_parcela.geom else None #Manejo de None
    updated_parcela_schema = Parcela.model_validate({
            "id": updated_parcela.id,
            "nombre": updated_parcela.nombre,
            "cultivo": updated_parcela.cultivo,
            "geom": parcela_wkt,
            "area": updated_parcela.area
        })

    return updated_parcela_schema

@router.delete("/{parcela_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parcela_endpoint(parcela_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_parcela(db, parcela_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parcela not found")
    return None