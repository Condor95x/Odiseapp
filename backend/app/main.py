import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

# Configuración básica del logging
logging.basicConfig(level=logging.DEBUG)  # Configura el nivel de log a 'DEBUG'
logger = logging.getLogger("myapp")  # Crea un logger llamado 'myapp'

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite tu frontend local
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

@app.get("/")
def read_root():
    logger.debug("Se ha llamado al endpoint raíz /")
    return {"message": "¡Bienvenido a la API de ODISEA!"}



# Registrar el enrutador
app.include_router(router, prefix="/api/v1")

# Agregar manejo global de excepciones si es necesario
@app.exception_handler(Exception)
async def log_exception(request, exc):
    logger.error(f"Excepción en el endpoint {request.url}: {str(exc)}")
    return {"detail": "Error interno en el servidor"}