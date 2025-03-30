from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import database
from .models.user import User, UserCreate, UserInDB

app = FastAPI(title="Totymark API")

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Totymark"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Rotas de usuário serão adicionadas aqui 