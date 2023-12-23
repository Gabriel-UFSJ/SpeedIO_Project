from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carregando as variáveis de ambiente
load_dotenv()

# Obtendo as variáveis de ambiente
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Conectando ao banco de dados
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
