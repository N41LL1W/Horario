import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

html_content = """
<main class="col-xs-12  col-md-9  col-md-push-3" role="main">
    <article class="clearfix post-1087 post type-post status-publish format-standard hentry category-linhas">
        Navegação: <a href="#ida">Itinerário de Ida</a> | <a href="#volta">Itinerário de Volta</a> | <a href="#horario">Horários</a><br /><br />
        <div class="hentry__content">
            <p><b>Tarifa:</b> R$ 7,00      (Reajuste em 01/07/2023)<br />
            <b>Tempo de Percurso:</b> Estimado: 1 hora <br />
            <b>Categoria:</b> Suburbana - Horários atualizados em 11/09/2023</p>
            <a name="ida"></a><p><h2 class="single .hentry">Itinerário de Ida</h2></p>
            <p>RIBEIRÃO PRETO<br />JARDINÓPOLIS</p>
            <a name="volta"></a><p><h2 class="single .hentry">Itinerário de Volta</h2></p>
            <p>JARDINÓPOLIS<br />RIBEIRÃO PRETO</p>
            <a name="horario"></a><p><h2 class="single .hentry">Horários de Segunda à Sexta</h2></p>
            <p>05:40 DIRETO<br />06:00 DIRETO<br />06:10 Não Passa no Morumbi<br />06:30 Jurucê / Estatua<br />06:40 S.Francisco<br />07:00 DIRETO<br />07:25 Jurucê <br />07:30 S.Francisco<br />07:50 S.Francisco<br />08:20 S.Fco não sobe Pernambucanas<br />08:45 S.Francisco<br />09:45 S.Francisco<br />10:25 S.Francisco<br />11:15 S.Francisco<br />12:30 S.Francisco<br />13:00 Jurucê / Estatua<br />13:30 S.Francisco<br />14:00 S.Francisco<br />14:45 S.Francisco<br />15:10 S.Francisco<br />15:20 Jurucê / Estatua<br />15:40 S.Francisco<br />16:00 S.Francisco<br />16:20 S.Francisco<br />16:40 S.Francisco<br />16:50 Jurucê / Estatua<br />16:56 S.Fco não sobe Pernambucanas<br />17:01 AROEIRA<br />17:08 S.Francisco<br />17:20 S.Francisco<br />17:30 S.Francisco<br />17:35 Jurucê / Mogiana<br />17:45 S.Fco não sobe Pernambucanas<br />17:50 S.Francisco<br />18:00 S.Francisco<br />18:01 VIA SHOPPING<br />18:15 S.Francisco<br />18:35 Jurucê / Estatua<br />18:45 S.Francisco<br />19:10 S.Francisco<br />20:00 S.Francisco<br />21:00 Jurucê / S.Fco / Morumbi<br />22:15 Renascer / S.Francisco <br />23:30 Renascer / S.Francisco <br /></p>
            <p><h2 class="single .hentry">Horários de Sábado</h2></p>
            <p>05:40 S.Francisco<br />06:00 S. Francisco<br />06:40 Jurucê / S.Fco<br />07:00 S.Francisco<br />07:45 S.Francisco<br />08:45 S.Francisco<br />09:20 S.Francisco<br />10:00 S.Francisco<br />11:00 S.Francisco<br />12:00 S. Francisco<br />12:30 S. Francisco<br />13:00 S.Francisco<br />13:30 Jurucê/Estatua<br />14:00 S.Francisco<br />14:30 S.Francisco<br />15:00 S.Francisco<br />16:00 S.Francisco<br />17:00 S.Francisco<br />18:00 S.Francisco<br />18:20 Jurucê/Estatua<br />19:00 S.Francisco<br />20:00 S.Francisco<br />21:00 Jurucê / S.Fco / Morumbi<br />23:30 Renascer São Francisco<br /></p>
            <p><h2 class="single .hentry">Horários de Domingo e Feriados</h2></p>
            <p>06:00 S. Francisco<br />07:00 Jurucê/ S.Fco./Morumbí<br />08:00 S. Francisco<br />09:30 S. Francisco<br />11:00 S. Francisco<br />13:30 S. Francisco<br />15:30 S. Francisco<br />18:00 S. Francisco<br />19:00 S. Francisco<br />21:00 Jurucê/ S.Fco./Morumbí<br />23:30 Renascer / S. Fco.<br /></p>
        </div>
    </article>
    <h4></h4>
</main>
"""

# Função para extrair horários
def extrair_horarios(titulo):
    horario_tag = soup.find('h2', string=titulo)
    if horario_tag:
        horarios_texto = horario_tag.find_next('p').get_text(separator="\n").strip()
        return horarios_texto.split("\n")
    return []

# Usando BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extrair horários
horarios_sexta = extrair_horarios('Horários de Segunda à Sexta')
horarios_sabado = extrair_horarios('Horários de Sábado')
horarios_domingo = extrair_horarios('Horários de Domingo e Feriados')

# Função para configurar e autenticar a API do Google Sheets
def google_sheets_auth():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

# Função para atualizar a planilha do Google Sheets
def atualizar_planilha():
    client = google_sheets_auth()
    sheet = client.open("RIBE_HORARIO").sheet1  # Abre a primeira aba da planilha
    
    # Criar uma lista para armazenar todas as linhas
    data = [["Horário", "Trajeto", "Dia da Semana"]]
    
    # Adicionar horários de Segunda à Sexta
    for horario in horarios_sexta:
        if len(horario.split()) > 1:
            trajeto = ' '.join(horario.split()[1:])
            horario_split = horario.split()[0]
        else:
            trajeto = ''
            horario_split = horario
        data.append([horario_split, trajeto, "Segunda à Sexta"])
    
    # Adicionar horários de Sábado
    for horario in horarios_sabado:
        if len(horario.split()) > 1:
            trajeto = ' '.join(horario.split()[1:])
            horario_split = horario.split()[0]
        else:
            trajeto = ''
            horario_split = horario
        data.append([horario_split, trajeto, "Sábado"])
    
    # Adicionar horários de Domingo e Feriados
    for horario in horarios_domingo:
        if len(horario.split()) > 1:
            trajeto = ' '.join(horario.split()[1:])
            horario_split = horario.split()[0]
        else:
            trajeto = ''
            horario_split = horario
        data.append([horario_split, trajeto, "Domingo e Feriados"])
    
    # Ordenar os dados por Dia da Semana e Horário
    data_sorted = sorted(data[1:], key=lambda x: (x[2], x[0]))
    data_sorted.insert(0, data[0])  # Reinsere o cabeçalho
    
    # Limpar a planilha antes de atualizar
    sheet.clear()
    
    # Adicionar os dados à planilha
    for row in data_sorted:
        sheet.append_row(row)

# Atualizar a planilha com os horários
atualizar_planilha()
