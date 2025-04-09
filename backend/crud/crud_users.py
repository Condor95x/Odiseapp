from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from models import Usuario
from schemas.schemas_users import UserResponse

async def get_users(db: AsyncSession) -> List[UserResponse]:
    result = await db.execute(select(Usuario))
    usuarios = result.scalars().all()

    # Convertir cada objeto Usuario a UserResponse
    user_responses = [
        UserResponse(
            id=usuario.id,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            rol=usuario.rol
        )
        for usuario in usuarios
    ]

    return user_responses