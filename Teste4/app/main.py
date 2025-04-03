import sys
from pathlib import Path
# Adiciona o diretório raiz ao sys.path 
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pymongo import MongoClient
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes.OperadorasAtivas import router as OperadorasAtivas
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import re

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de logs
LOG_FILE = "app.log"
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Resposta gerada com status: {response.status_code}")
    return response

# Caminho do arquivo
RESOURCE_DIR = Path("resources") 
CSV_FILE = RESOURCE_DIR / "Relatorio_cadop.csv"

@app.on_event("startup")
async def startup_db_client():
    if CSV_FILE.exists():
        print("Arquivo encontrado: Conectado ao banco de dados!")
    else:
        print("Arquivo não encontrado!")

@app.on_event("shutdown")
async def shutdown_db_client():
    print("Disconnected to the database!")

@app.get("/")
async def homepage():
    logger.info("Endpoint /hello-world acessado")
    return {"message": "welcome to our homepage"}

# Função para normalizar as chaves do JSON
def normalize_keys(data):
    return {re.sub(r'(?<!^)(?=[A-Z])', '_', k).lower(): v for k, v in data.items()}

# Middleware para normalizar as chaves de todas as requisições JSON
@app.middleware("http")
async def normalize_request_data(request: Request, call_next):
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
            if isinstance(body, dict):
                request._json = normalize_keys(body)
            elif isinstance(body, list):
                request._json = [normalize_keys(item) for item in body]
        except Exception as e:
            logger.error(f"Erro ao normalizar requisição: {e}")
    
    return await call_next(request)

app.include_router(OperadorasAtivas, prefix="/OperadorasAtivas", tags=["OperadorasAtivas"])
