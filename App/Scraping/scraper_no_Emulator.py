import requests
from bs4 import BeautifulSoup

# Set dos headers para a requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'TE': 'Trailers'
}

# Função para obter os dados do site
def scrape_similarweb(url):
    base_url = "https://www.similarweb.com/website/"
    full_url = base_url + url
    print(full_url)

    try:
        # Fazendo a requisição
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup.prettify())

        # Função para obter o texto de um elemento a partir do ID
        def get_element_text(soup, element_id):
            div = soup.find('div ', id=element_id).get_text()
            return div
        
        # Lista de IDs dos elementos
        element_ids = ['overview', 'ranking', 'traffic', 'geography', 'demographics', 'interests', 
                       'competitors', 'traffic-sources', 'keywords', 'referrals', 'social-media', 'outgoing-links', 'technologies']
        
        # Dicionário para armazenar os dados
        data = {}
        for element_id in element_ids:
            data[element_id] = get_element_text(soup, element_id)
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {full_url}: {e}")
        return None

    
