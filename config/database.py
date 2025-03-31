from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging
from urllib.parse import quote_plus

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "totymark")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL não está definida nas variáveis de ambiente")

try:
    # Codifica a URL para garantir que caracteres especiais sejam tratados corretamente
    encoded_url = quote_plus(MONGODB_URL)
    client = AsyncIOMotorClient(encoded_url, serverSelectionTimeoutMS=5000)
    
    # Testa a conexão
    client.admin.command('ping')
    
    database = client[DATABASE_NAME]
    logger.info(f"Conectado ao banco de dados {DATABASE_NAME}")
except Exception as e:
    logger.error(f"Erro ao conectar ao MongoDB: {str(e)}")
    raise

# Coleções
users_collection = database.users
messages_collection = database.messages

async def get_database():
    return database

async def close_database():
    client.close() 