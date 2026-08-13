from utils import add_data, load_data, load_template, build_response
from urllib.parse import unquote_plus


def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'): # Se vor Post
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = unquote_plus(chave_valor[1])     # subtstitui caract espec auto       
        add_data({'titulo': params['titulo'], 'detalhes': params['detalhes']})

        return build_response(code=303, reason='See Other', headers='Location: /')

    
    notes_li = [load_template('components/note.html').format(title=dados['titulo'], details=dados['detalhes']) for dados in load_data('notes.json')]
    notes = '\n'.join(notes_li)
    return build_response(load_template('index.html').format(notes=notes))
