from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from models import Parcela
from schemas import ParcelaCreate, ParcelaUpdate
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape

async def create_parcela(db: AsyncSession, parcela: ParcelaCreate):
    db_parcela = Parcela(nombre=parcela.nombre, cultivo=parcela.cultivo, geom=WKTElement(parcela.geom, srid=4326))
    db.add(db_parcela)
    await db.commit()
    await db.refresh(db_parcela)
    return {"status": 201, "message": "Added successfully"}

async def get_parcelas(db: AsyncSession):
    result = await db.execute(select(Parcela))
    parcelas = result.scalars().all()
    for obj in parcelas:
        if isinstance(obj.geom, str):
            obj.geom = WKTElement(obj.geom)
        obj.geom = to_shape(obj.geom).wkt
    return parcelas

async def get_parcela(db: AsyncSession, parcela_id: int):
    result = await db.execute(select(Parcela).where(Parcela.id == parcela_id))
    parcela_db = result.scalars().first()
    return parcela_db  # Retorna el objeto del modelo (o None si no existe)

async def update_parcela(db: AsyncSession, parcela_id: int, parcela_update: ParcelaUpdate):
    existing_parcela = await db.get(Parcela, parcela_id)
    if existing_parcela is None:
        return None # Retorna None si no existe

    for key, value in parcela_update.dict(exclude_unset=True).items():
        if key == "geom":
            if value is not None:
                existing_parcela.geom = WKTElement(value, srid=4326)
            else:
                existing_parcela.geom = None
        else:
            setattr(existing_parcela, key, value)

    await db.commit()
    await db.refresh(existing_parcela)
    return existing_parcela # Retorna el modelo actualizado

async def delete_parcela(db: AsyncSession, parcela_id: int):
    parcela = await db.get(Parcela, parcela_id)
    if parcela is None:
        return False  # Indica que no se encontró la parcela
    await db.delete(parcela)
    await db.commit()
    return True  # Indica que la eliminación fue exitosa