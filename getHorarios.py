import requests
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

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

# Função para configurar e autenticar a API do Google Sheets
def google_sheets_auth():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_path = 'credentials.json'  # Certifique-se de que este caminho está correto

    # Verifique se o arquivo existe no caminho especificado
    if not os.path.isfile(credentials_path):
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credentials_path}")

    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    return client

# Função para atualizar a planilha do Google Sheets
def atualizar_planilha(horarios_jardinopolis, horarios_linha_01):
    client = google_sheets_auth()
    sheet = client.open("RIBE_HORARIO").sheet1  # Abre a primeira aba da planilha
    data = []

    # Adicionar linha com o título do site
    data.append(["Ribeirão a Jardinópolis", "", "", "", "", "", "Linha 01", "", "", "", "", ""])
    
    # Mesclar células para o título
    sheet.merge_cells(1, 1, 1, 6)  # Mescla de A1 a F1
    sheet.merge_cells(1, 7, 1, 12) # Mescla de G1 a L1
    
    # Adicionar linha com os dias da semana
    days_of_week = ["Segunda à Sexta", "", "Sábado", "", "Domingo e Feriados", "", "Segunda à Sexta", "", "Sábado", "", "Domingo e Feriados", ""]
    data.append(days_of_week)

    # Mesclar células para os dias da semana
    for i in range(0, 12, 2):
        sheet.merge_cells(2, i + 1, 2, i + 2)

    # Cabeçalhos com diferenciação
    headers = [
        "Horários", "Trajeto", 
        "Horários", "Trajeto", 
        "Horários", "Trajeto",
        "Horários", "Trajeto", 
        "Horários", "Trajeto", 
        "Horários", "Trajeto"
    ]
    data.append(headers)

    # Adicionar horários e trajetos para cada dia da semana
    max_rows = max(
        len(horarios_jardinopolis['sexta']),
        len(horarios_jardinopolis['sabado']),
        len(horarios_jardinopolis['domingo']),
        len(horarios_linha_01['sexta']),
        len(horarios_linha_01['sabado']),
        len(horarios_linha_01['domingo'])
    )

    for i in range(max_rows):
        row = []

        # Segunda à Sexta - Ribeirão a Jardinópolis
        if i < len(horarios_jardinopolis['sexta']):
            row.extend(horarios_jardinopolis['sexta'][i])
        else:
            row.extend(["", ""])
        
        # Sábado - Ribeirão a Jardinópolis
        if i < len(horarios_jardinopolis['sabado']):
            row.extend(horarios_jardinopolis['sabado'][i])
        else:
            row.extend(["", ""])
        
        # Domingo e Feriados - Ribeirão a Jardinópolis
        if i < len(horarios_jardinopolis['domingo']):
            row.extend(horarios_jardinopolis['domingo'][i])
        else:
            row.extend(["", ""])

        # Segunda à Sexta - Linha 01
        if i < len(horarios_linha_01['sexta']):
            row.extend(horarios_linha_01['sexta'][i])
        else:
            row.extend(["", ""])
        
        # Sábado - Linha 01
        if i < len(horarios_linha_01['sabado']):
            row.extend(horarios_linha_01['sabado'][i])
        else:
            row.extend(["", ""])
        
        # Domingo e Feriados - Linha 01
        if i < len(horarios_linha_01['domingo']):
            row.extend(horarios_linha_01['domingo'][i])
        else:
            row.extend(["", ""])
        
        # Verifica se há dados na linha antes de adicionar à planilha
        if any(row):
            data.append(row)

    # Atualizar a planilha
    sheet.clear()
    sheet.append_rows(data)

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

    # Atualizar a planilha com os horários e trajetos
    atualizar_planilha(horarios_jardinopolis, horarios_linha_01)

if __name__ == "__main__":
    main()
