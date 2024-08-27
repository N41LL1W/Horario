import requests
from bs4 import BeautifulSoup
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# URLs dos sites com os horários
urls = [
    ("https://www.ribetransporte.com.br/ribeirao-preto-a-jardinopolis/", "Ribeirão a Jardinópolis"),
    ("https://www.ribetransporte.com.br/linha-01/", "Linha 01")
]

# Função para buscar o conteúdo HTML do site
def buscar_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Erro ao acessar o site: {response.status_code}")

# Função para extrair dados dos horários e trajetos
def extrair_dados(titulo, soup):
    horario_tag = soup.find('h2', string=titulo)
    if horario_tag:
        horarios_texto = horario_tag.find_next('p').get_text(separator="\n").strip()
        return horarios_texto.split("\n")
    return []

# Função para dividir horários e trajetos
def extrair_horario_e_trajeto(linha):
    match = re.match(r"(\d{2}:\d{2})\s*(.*)", linha)
    if match:
        horario = match.group(1)
        trajeto = match.group(2).strip()
        return horario, trajeto
    return linha, ""

# Função para configurar e conectar ao MongoDB
def mongo_connect():
    uri = "mongodb+srv://willian_play_cel:#Bi13Ga08Wi87@cluster0.nriahc4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    db = client["horarios_db"]
    return db

# Função para salvar os dados no MongoDB
def salvar_no_mongo(db, collection_name, data):
    collection = db[collection_name]
    collection.insert_many(data)

# Função principal para buscar, processar e atualizar os dados
def main():
    horarios_jardinopolis = {'sexta': [], 'sabado': [], 'domingo': []}
    horarios_linha_01 = {'sexta': [], 'sabado': [], 'domingo': []}

    # Processar cada URL
    for url, title in urls:
        html_content = buscar_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')

        if "ribeirao-preto-a-jardinopolis" in url:
            horarios_jardinopolis['sexta'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Segunda à Sexta', soup) if "Observação" not in linha]
            horarios_jardinopolis['sabado'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Sábado', soup) if "Observação" not in linha]
            horarios_jardinopolis['domingo'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Domingo e Feriados', soup) if "Observação" not in linha]
        elif "linha-01" in url:
            horarios_linha_01['sexta'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Segunda à Sexta', soup) if "Observação" not in linha]
            horarios_linha_01['sabado'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Sábado', soup) if "Observação" not in linha]
            horarios_linha_01['domingo'] = [extrair_horario_e_trajeto(linha) for linha in extrair_dados('Horários de Domingo e Feriados', soup) if "Observação" not in linha]

    # Conectar ao MongoDB
    db = mongo_connect()

    # Salvar os dados no MongoDB
    salvar_no_mongo(db, "horarios_jardinopolis", horarios_jardinopolis)
    salvar_no_mongo(db, "horarios_linha_01", horarios_linha_01)

if __name__ == "__main__":
    main()
