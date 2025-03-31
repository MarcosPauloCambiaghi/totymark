from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from config.database import users_collection, messages_collection
from config.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    type: str = "text"  # text, pix, notification

class Message(MessageBase):
    id: str
    timestamp: datetime
    read: bool = False

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    active: bool = True
    last_seen: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PixNotification(BaseModel):
    amount: float
    description: str
    sender_name: str
    pix_key: str
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None

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
            "docs": "/docs",
            "token": "/token"
        }
    }

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await users_collection.find_one({"username": form_data.username})
        if not user or not verify_password(form_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Erro no login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    try:
        db_user = await users_collection.find_one({"username": user.username})
        if db_user:
            raise HTTPException(status_code=400, detail="Usuário já existe")
        
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_password
        user_dict["active"] = True
        user_dict["last_seen"] = datetime.utcnow()
        
        result = await users_collection.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        return User(**user_dict)
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@app.get("/users", response_model=List[User])
async def get_users(current_user: str = Depends(get_current_user)):
    try:
        users = []
        cursor = users_collection.find({})
        async for user in cursor:
            user["id"] = str(user["_id"])
            users.append(User(**user))
        return users
    except Exception as e:
        logger.error(f"Erro ao buscar usuários: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@app.get("/messages", response_model=List[Message])
async def get_messages(current_user: str = Depends(get_current_user)):
    try:
        messages = []
        cursor = messages_collection.find({})
        async for message in cursor:
            message["id"] = str(message["_id"])
            messages.append(Message(**message))
        return messages
    except Exception as e:
        logger.error(f"Erro ao buscar mensagens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@app.post("/messages", response_model=Message)
async def create_message(
    message: MessageBase,
    current_user: str = Depends(get_current_user)
):
    try:
        message_dict = message.dict()
        message_dict["timestamp"] = datetime.utcnow()
        message_dict["read"] = False
        
        result = await messages_collection.insert_one(message_dict)
        message_dict["id"] = str(result.inserted_id)
        return Message(**message_dict)
    except Exception as e:
        logger.error(f"Erro ao criar mensagem: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@app.post("/notify-pix", response_model=Message)
async def notify_pix(
    notification: PixNotification,
    current_user: str = Depends(get_current_user)
):
    try:
        # Criar mensagem para o banco de dados
        message_dict = {
            "content": f"PIX recebido: R$ {notification.amount:.2f} de {notification.sender_name}",
            "sender_id": current_user,
            "type": "pix",
            "timestamp": datetime.utcnow(),
            "read": False
        }
        
        result = await messages_collection.insert_one(message_dict)
        message_dict["id"] = str(result.inserted_id)
        
        # Enviar notificação por email se fornecido
        if notification.email:
            try:
                # Email principal
                msg = MIMEMultipart()
                msg['From'] = "cambiaghimarcos@gmail.com"
                msg['To'] = notification.email
                msg['Subject'] = "💰 PIX Recebido - Totymark"
                
                body = f"""
                🎉 PIX Recebido com Sucesso!
                
                💰 Valor: R$ {notification.amount:.2f}
                👤 Remetente: {notification.sender_name}
                🔑 Chave PIX: {notification.pix_key}
                📝 Descrição: {notification.description}
                ⏰ Data: {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')}
                
                Obrigado por usar o Totymark!
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Configuração do Gmail com suas credenciais
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login("cambiaghimarcos@gmail.com", "Mark288033")
                server.send_message(msg)
                
                # Email de encaminhamento
                forward_msg = MIMEMultipart()
                forward_msg['From'] = "cambiaghimarcos@gmail.com"
                forward_msg['To'] = "cambiaghimar38@gmail.com"
                forward_msg['Subject'] = "📨 PIX Encaminhado - Totymark"
                
                forward_body = f"""
                📨 PIX Encaminhado
                
                💰 Valor: R$ {notification.amount:.2f}
                👤 Remetente: {notification.sender_name}
                📧 Email Original: {notification.email}
                🔑 Chave PIX: {notification.pix_key}
                📝 Descrição: {notification.description}
                ⏰ Data: {datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S')}
                """
                
                forward_msg.attach(MIMEText(forward_body, 'plain'))
                server.send_message(forward_msg)
                server.quit()
                
            except Exception as e:
                logger.error(f"Erro ao enviar email: {str(e)}")
        
        # Enviar notificação por WhatsApp se fornecido
        if notification.whatsapp:
            try:
                # Link direto para o WhatsApp
                whatsapp_api_url = "https://api.whatsapp.com/send"
                message = f"💰 PIX Recebido!\n\nValor: R$ {notification.amount:.2f}\nDe: {notification.sender_name}\nData: {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}"
                url = f"{whatsapp_api_url}?phone={notification.whatsapp}&text={message}"
                requests.get(url)
                
            except Exception as e:
                logger.error(f"Erro ao enviar WhatsApp: {str(e)}")
        
        return Message(**message_dict)
        
    except Exception as e:
        logger.error(f"Erro ao processar notificação PIX: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar notificação PIX"
        )

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081) 