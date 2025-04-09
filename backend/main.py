from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import operaciones_router, router_plot, router_grapevines, router_vineyard ,router_inventory, router_users,router_tasklist,router_winery
from authentification import auth
from database import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # Origen de tu frontend
    "http://127.0.0.1:3000", #  Origen de tu frontend (con 127.0.0.1)
    "http://127.0.0.1", #  Origen de tu frontend (sin puerto)
]
app.include_router(router_winery.router, tags=["winery"])
app.include_router(router_inventory.router, tags=["inventory"])
app.include_router(router_tasklist.router, tags=["task"])
app.include_router(router_users.router, tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(router_plot.router, prefix="/plots", tags=["plots"])
app.include_router(router_grapevines.router, prefix="/grapevines", tags=["grapevines"])
app.include_router(router_vineyard.router, prefix="/vineyard", tags=["vineyard"])
app.include_router(operaciones_router.router, prefix="/operaciones", tags=["operaciones"])


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