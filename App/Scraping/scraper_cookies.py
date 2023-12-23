from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import os

# Set dos headers para a requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

# Função para obter os cookies do site
def get_cookies_selenium(url):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    driver_path = os.path.join(script_dir, '..', '..', 'selenium', 'chromedriver.exe')

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    service = ChromeService(executable_path=driver_path)

    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)

        # Obtendo todos os cookies
        cookies = driver.get_cookies()
        return cookies

    except Exception as e:
        print(f"Erro ao obter cookies: {e}")
        return None

    finally:
        if driver:
            driver.quit()

# Função para obter os dados do site com os cookies
def scrape_similarweb_with_cookies(url, cookies):
    base_url = "https://www.similarweb.com/website/"
    full_url = base_url + url

    try:
        session = HTMLSession()

        # Adicionando os cookies à sessão
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Obtendo os cookies adicionais de interações com o site
        first_session = session.get('https://www.similarweb.com/_sec/cp_challenge/ak-challenge-4-1.html', headers=headers).cookies
        session.cookies.set('bm_sv', first_session['bm_sv'])
        second_session = session.get('https://www.similarweb.com/_sec/cp_challenge/ak-challenge-4-1.js', headers=headers).cookies
        session.cookies.set('ak_bmsc', second_session['ak_bmsc'])

        # Fazendo a solicitação para a página
        response = session.get(full_url, headers=headers, cookies=session.cookies)

        # Conteúdo da página
        main_page_content = response.html.html

        soup = BeautifulSoup(main_page_content, 'html.parser')
        print(soup.prettify())

        # Função para obter o texto de um elemento a partir do ID
        def get_element_text(soup, element_id):
            return soup.find(id=element_id).get_text()
        
        # Lista de IDs dos elementos
        element_ids = ['overview', 'ranking', 'traffic', 'geography', 'demographics', 'interests', 
                       'competitors', 'traffic-sources', 'keywords', 'referrals', 'social-media', 'outgoing-links', 'technologies']
        
        # Dicionário para armazenar os dados
        data = {}
        for element_id in element_ids:
            data[element_id] = get_element_text(soup, element_id)

        return data

    except Exception as e:
        print(f"Erro ao acessar {full_url}: {e}")

    finally:
        session.close()
