from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Totymark API",
    description="API para sistema de mensagens em tempo real",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class MessageBase(BaseModel):
    content: str
    sender_id: str

class Message(MessageBase):
    id: str
    timestamp: datetime
    read: bool = False

class UserBase(BaseModel):
    username: str
    email: str

class User(UserBase):
    id: str
    active: bool = True
    last_seen: Optional[datetime] = None

# Rotas da API
@app.get("/")
def root():
    return {
        "app": "Totymark",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "messages": "/messages",
            "users": "/users",
            "docs": "/docs"
        }
    }

@app.get("/messages", response_model=List[Message])
def get_messages():
    # TODO: Implementar busca de mensagens no MongoDB
    return []

@app.get("/users", response_model=List[User])
def get_users():
    # TODO: Implementar busca de usuários no MongoDB
    return []

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 