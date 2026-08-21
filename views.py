from utils import add_data, load_data, load_template, build_response
from urllib.parse import unquote_plus
import database 

# Tratar requests
def index(request):
    # Adiciona cartas do banco de dados ao html
    sql_entity = database.Database('data/banco')
    notes_li = []
    for dados in sql_entity.get_all():
        notes_li.append(
            load_template('components/note.html').format(
                title=dados.title,
                details=dados.content,
                id=dados.id
            )
        )
    notes = '\n'.join(notes_li)

    # Trata requisição 'POST'
    if request.startswith('POST'): 
        # Trata texto da requisição
        request = request.replace('\r', '')     # Remove caracteres indesejados
        partes = request.split('\n\n')          # Cabeçalho e corpo separados por duas quebras de linha
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            chave_valor = chave_valor.split('=')
            params[chave_valor[0]] = unquote_plus(chave_valor[1])     # subst. caract espec auto       

        # Monta resposta por ''subtipo'' (valor parametro) de POST
        # Criar Nota
        if params['acao'] == 'criar':
            note = database.Note(title=params['titulo'], content=params['detalhes'])
            sql_entity.add(note)

        # Excluir Nota
        elif params['acao'] == 'excluir':
            id_note = int(params['id'])
            sql_entity.delete(id_note)

        # Retorna resposta montada
        return build_response(code=303, reason='See Other', headers='Location: /')

    return build_response(load_template('index.html').format(notes=notes))
