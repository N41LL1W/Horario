# Horários de Transporte - HORARIO

Este projeto consiste em um script Python para extrair horários de transporte de dois sites diferentes e atualizar uma planilha no Google Sheets com esses dados. O objetivo é automatizar o processo de manutenção de informações de horários e trajetos de transporte público.

## Funcionalidades

- **Extração de Dados**: O script faz o parsing de dois sites diferentes para extrair informações de horários e trajetos de transporte público.
- **Atualização Automática**: Os dados extraídos são atualizados em tempo real em uma planilha do Google Sheets, permitindo fácil visualização e compartilhamento.
- **Organização por Dia da Semana**: Os horários são organizados por dia da semana (Segunda à Sexta, Sábado, Domingo e Feriados), facilitando a consulta por usuários.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para a extração e manipulação dos dados.
- **Beautiful Soup**: Biblioteca Python para scraping de dados HTML e XML.
- **Requests**: Biblioteca Python para realizar requisições HTTP.
- **Google Sheets API**: API utilizada para atualizar a planilha do Google Sheets.
- **Markdown**: Formato de arquivo utilizado para este `README.md`, facilitando a formatação de texto.

## Como Usar

1. **Configuração Inicial**:
   - Instale as bibliotecas necessárias:
     ```
     pip install beautifulsoup4 requests gspread oauth2client
     ```
   - Configure o arquivo `credentials.json` para autenticação na API do Google Sheets.

2. **Execução do Script**:
   - Execute o script `horarios_transportes.py` para extrair os dados dos sites e atualizar a planilha.

3. **Verificação na Planilha**:
   - Acesse a planilha "RIBE_HORARIO" no Google Sheets para verificar os horários atualizados.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para fazer fork deste repositório e enviar pull requests com melhorias, correções de bugs ou novas funcionalidades.

## Autor

Desenvolvido por [Willian Gomes](https://github.com/N41LL1W).

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
