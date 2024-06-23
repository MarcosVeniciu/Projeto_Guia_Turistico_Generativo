import proxies
import time
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search

# Carregar dados dos hotéis
df = pd.read_csv("Dataset/Hoteis/lista_hoteis.csv")
lista_hoteis = df["hotel"]
print(f"Total de hoteis: {len(lista_hoteis)}")

# Função para testar se o proxy está funcionando
def test_proxy(proxy):
    try:
        response = requests.get('http://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

# Função para realizar a busca no Google com proxies
def perform_search(query, num_results=8, lang='en', retries=3, proxies=None):
    delay = 30  # Inicial delay
    for attempt in range(retries):
        if proxies:
            for proxy in proxies:
                if not test_proxy(proxy):
                    print(f"Proxy {proxy} não está funcionando. Tentando o próximo...")
                    continue
                # Configurando o proxy para a sessão de requisição
                session = requests.Session()
                session.proxies = {'http': proxy, 'https': proxy}
                try:
                    # Utilizando a sessão para realizar a busca
                    return list(search(query, num_results=num_results, lang=lang))
                except Exception as e:
                    print(f"Erro durante a busca com o proxy {proxy}: {e}")
                    if "429" in str(e):
                        print(f"Too many requests. Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay += 0  # Exponential backoff
        else:
            try:
                return list(search(query, num_results=num_results, lang=lang))
            except Exception as e:
                print(f"Erro durante a busca: {e}")
                if "429" in str(e):
                    print(f"Too many requests. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay += 0  # Exponential backoff
    print("Exceeded maximum retries for query:", query)
    return []




with open('resultados_hoteis.csv', 'w', newline='') as csvfile:
    # Criar objeto de escrita do CSV
    writer = csv.writer(csvfile)
    # Escrever cabeçalho da tabela
    writer.writerow(['Nome do Hotel', 'URL'])

    for i in range(0, len(lista_hoteis)):
        hotel = lista_hoteis[i]
        print(f"({i+1}/{len(lista_hoteis)}): {hotel}")
        query = f"{hotel}, in cabo frio brazil site: booking.com, almosafer.com"
        sites_bons = ["booking.com", "almosafer.com"]

        # Realizar busca no Google com tentativas de repetição
        resultados = perform_search(query, proxies=proxies.proxies)
        if not resultados:
            print(f"Não foi possível obter resultados para o hotel: {hotel}")
            continue

        for url in resultados:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else 'No title'

                print(f"Título: {title}")
                print(f"Link: {url}")
                print("------------------------")
                for substring in sites_bons:
                    if substring in url:
                        # Escrever cada linha no CSV
                        writer.writerow([hotel, url])
            except Exception as e:
                print(f"Erro ao processar {url}: {e}")
                print("------------------------")
            # Intervalo para evitar limites de taxa
            time.sleep(10)
        # Intervalo adicional entre diferentes buscas de hotéis
        time.sleep(50)

