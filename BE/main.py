from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import parcelas
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
@app.get("/")
def read_root():
    return {"vamo de nuevo"}

app.include_router(parcelas.router, prefix="/parcelas", tags=["parcelas"]) #include router