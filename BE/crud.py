from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Parcela
from schemas import ParcelaCreate
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape

async def create_parcela(db: AsyncSession, item: ParcelaCreate):
    db_item = Parcela(nombre=item.nombre, geom=WKTElement(item.geom, srid=4326), cultivo=item.cultivo)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return {"status": 201,"message":'Added successfully'}

async def get_Parcelas(db: AsyncSession):
    result = await db.execute(select(Parcela))
    items = result.scalars().all()
    parcelas_list = []
    for item in items:
        # Conviertir la geometría a WKT para la respuesta API. Manejar valores None.
        geom_wkt = to_shape(item.geom).wkt if item.geom else None
        parcela_dict = {
            "id": item.id,
            "nombre": item.nombre,
            "Cultivo": item.cultivo,
            "geom": geom_wkt,
            "area": item.area
        }
        parcelas_list.append(parcela_dict)
    return parcelas_list