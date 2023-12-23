from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import re

def scrape_similarweb_selenium(url, clean_data):
    base_url = "https://www.similarweb.com/website/"
    full_url = base_url + url

    # Obtendo o diretório do script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Configurando o caminho para o executável do ChromeDriver
    driver_path = os.path.join(script_dir, '..', '..', 'selenium', 'chromedriver.exe')

    # Configurando as opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Inicializando o service do Chrome
    service = ChromeService(executable_path=driver_path)

    driver = None

    try:
        # Inicializando o driver do Chrome com o service configurado
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Acessando a URL
        driver.get(full_url)

        # Aguarde até 10 segundos para permitir que a página seja carregada
        driver.implicitly_wait(10)

        title = driver.title
        print("Título:", title)
        print("HTML content: ", driver.page_source)

        # Função para obter o texto de um elemento a partir do ID
        def get_element_text(driver, element_id):
            return driver.find_element(By.ID, element_id).text
        
        # Lista de IDs dos elementos
        element_ids = ['overview', 'ranking', 'traffic', 'geography', 'demographics', 'interests', 'competitors', 
                       'traffic-sources', 'keywords', 'referrals', 'social-media', 'outgoing-links', 'technologies']
        
        # Dicionário para armazenar os dados
        data = {}
        data = {'url': url}
        for element_id in element_ids:
            data[element_id] = get_element_text(driver, element_id)

        print(data)

        if clean_data:
            data = limpar_dados(data)

    except Exception as e:
        print(f"Erro ao acessar {full_url}: {e}")

    finally:
        # Fechando o navegador
        if driver:
            driver.quit()

    return data

def limpar_dados(dados_brutos):
    if not isinstance(dados_brutos, dict):
        raise ValueError("A entrada deve ser um dicionário.")

    dados_limpos = {}

    for chave, valor in dados_brutos.items():
        if isinstance(valor, str):
            # Substituir caracteres indesejados
            valor_limpo = re.sub(r'\n+', '\n', valor)  # Remover linhas duplicadas
            valor_limpo = re.sub(r'\n(?=[A-Za-z])', ' ', valor_limpo)  # Substituir quebras de linha por espaços
            valor_limpo = re.sub(r'\n', '', valor_limpo)  # Remover quebras de linha restantes
            valor_limpo = re.sub(r'\s{2,}', ' ', valor_limpo)  # Substituir múltiplos espaços por um único espaço

            dados_limpos[chave] = valor_limpo.strip()  # Remover espaços em branco no início e no final
        else:
            dados_limpos[chave] = valor  # Manter valores que não são strings sem alterações

    return dados_limpos