from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    rol: str

    class Config:
        orm_mode = True