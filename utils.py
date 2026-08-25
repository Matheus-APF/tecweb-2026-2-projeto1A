import json
from urllib.parse import unquote_plus

def extract_route(request):
    # Busca o Patche na string da requisição e devolve
    i0 = request.find('/') + 1
    i1 = request.find(' HTTP')
    return request[i0:i1]

def read_file(path):
    # with open garante fechamento
    # abre arquivo como bytes --> le os dados --> retorna
    with open(path, 'rb') as file:
        return file.read()

def load_template(name):
    with open(f'templates/{name}', 'r', encoding='utf-8') as file:
        return file.read()

def load_data(name):
    return json.load(open(f'data/{name}'))  

def add_data(note):
    notes = load_data('notes.json')
    notes.append(note)
    with open('data/notes.json', 'w') as file:
        json.dump(notes, file)

def build_response(body='', code=200, reason='OK', headers=''):
    # Monta Response com arquivo solicitado no formato HTTP *S/ Body ainda
    response = f'HTTP/1.1 {code} {reason}\n{headers}\n{body}'
    return response.encode()

def extrair_params(request):
    """Extrai os parâmetros enviados no corpo de uma requisição POST."""
    request = request.replace('\r', '')  # Padroniza as quebras de linha
    partes = request.split('\n\n')       # Separa cabeçalho e corpo
    corpo = partes[1]
    params = {}
    # Converte "titulo=ABC&detalhes=XYZ" em um dicionário
    for chave_valor in corpo.split('&'):
        chave, valor = chave_valor.split('=')
        params[chave] = unquote_plus(valor)  # Decodifica caracteres especiais
    return params