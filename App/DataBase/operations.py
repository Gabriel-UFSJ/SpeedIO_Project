from .mongo import db

# Funções de operações no banco de dados

# Função para inserir dados no banco de dados
def insert(collection_name, data):
    collection = db[collection_name]
    result = collection.insert_one(data)
    return result.inserted_id

# Função para encontrar dados no banco de dados
def find_data(collection_name, query):
    collection = db[collection_name]
    result = collection.find_one(query)
    if result:
        result['_id'] = str(result['_id'])
    return result