from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import Parcela, ParcelaCreate
from crud import create_parcela, get_Parcelas

router = APIRouter()

#crear una nueva parcela
@router.post("/")
async def create_new_parcela(item: ParcelaCreate, db: AsyncSession = Depends(get_db)):
    res = await create_parcela(db, item)
    return res

#Obtener todas las parcelas
@router.get("/")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await get_Parcelas(db)