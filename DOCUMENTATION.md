# Documentação do Projeto Totymark

## Estrutura do Projeto
```
totymark/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   └── database.py
│   └── models/
│       └── user.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Arquivos Criados

### 1. backend/config/database.py
```python
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "totymark")

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Coleções
users_collection = database.users
messages_collection = database.messages
chats_collection = database.chats
```

### 2. backend/models/user.py
```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    is_active: bool = True

class User(UserBase):
    id: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
```

### 3. backend/main.py
```python
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
```

### 4. .env
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=totymark
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. backend/__init__.py
```python
"""
Totymark - Sistema de mensagens em tempo real
"""

__version__ = "0.1.0"
```

## Próximos Passos

### 1. Configuração do Ambiente
1. Instalar as dependências:
```bash
pip install -r requirements.txt
```

2. Garantir que o MongoDB está rodando:
```bash
sudo service mongodb start
```

### 2. Testando o Backend
1. Iniciar o servidor:
```bash
uvicorn backend.main:app --reload
```

2. Acessar a documentação da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Endpoints Disponíveis
- GET `/`: Mensagem de boas-vindas
- GET `/health`: Verificação de saúde da API

## Dependências Principais
- FastAPI
- MongoDB (Motor)
- Python-dotenv
- Pydantic
- Uvicorn
- WebSockets

## Observações
- O backend está configurado com CORS permitindo todas as origens (deve ser restrito em produção)
- A chave secreta no arquivo .env deve ser alterada em produção
- O MongoDB está configurado para rodar localmente na porta padrão 27017 