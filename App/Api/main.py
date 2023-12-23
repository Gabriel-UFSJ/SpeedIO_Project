import sys
sys.path.append("..")

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from Scraping.scraper import scrape_similarweb_selenium
from DataBase.operations import insert, find_data
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configuração para permitir solicitações de qualquer origem (CORS)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definindo os modelos de entrada e saída
class ScrapingRequest(BaseModel):
    url: str
    clean_data: bool

class ScrapingResponse(BaseModel):
    message: str

# Definindo a rota para o scraping
@app.post("/salve_info", response_model=ScrapingResponse)
async def scrape_and_save_info(request: ScrapingRequest):
    try:
        # Obter dados do scraping
        scraped_data = scrape_similarweb_selenium(request.url, request.clean_data)

        # Salvar os dados no MongoDB
        insert("scraped_data", scraped_data)

        return JSONResponse(content=jsonable_encoder({"message": "Dados salvos com sucesso"}), status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a solicitação: {str(e)}")

# Definindo os modelos de entrada e saída
class GetInfoRequest(BaseModel):
    url: str

class GetInfoResponse(BaseModel):
    data: dict

# Definindo a rota para obter os dados
@app.post("/get_info", response_model=GetInfoResponse)
async def get_info(request: GetInfoRequest):
    try:
        # Procurando os dados no MongoDB
        query = {"url": request.url}
        data = find_data("scraped_data", query)

        if data:
            return JSONResponse(content=jsonable_encoder({"data": data}), status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados no banco de dados.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar a solicitação: {str(e)}")
