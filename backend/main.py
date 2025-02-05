from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import parcelas # add router

from database import engine, Base

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importa el middleware CORS


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # Origen de tu frontend
    "http://localhost:3000", #  Origen de tu frontend (con www si lo usas)
    "http://localhost", #  Origen de tu frontend (sin puerto)
    "http://127.0.0.1:3000", #  Origen de tu frontend (con 127.0.0.1)
    "http://127.0.0.1", #  Origen de tu frontend (sin puerto)
    "*",  # Esto permite todos los origenes (solo para desarrollo, no para producción)
]

app.include_router(parcelas.router, prefix="/parcelas", tags=["parcelas"]) # include router

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Si necesitas enviar cookies o encabezados de autenticación
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)