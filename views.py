from utils import add_data, load_data, load_template, build_response, extrair_params
import database 

# TRATA REQUEST

# Tela Index
def index(request):
    # Conecta ao banco de dadoss
    sql_entity = database.Database('data/banco')
    
    # Trata requisição 'POST'
    if request.startswith('POST'): 
        # Extrai parametros
        params = extrair_params(request)

        # Monta resposta por ''subtipo'' (parametro acao)
        # Criar Nota
        if params['acao'] == 'criar':
            note = database.Note(title=params['titulo'], content=params['detalhes'])
            sql_entity.add(note)

        # Excluir Nota
        elif params['acao'] == 'excluir':
            id_note = int(params['id'])
            sql_entity.delete(id_note)

        # Retorna resposta montada
        #return build_response(code=303, reason='See Other', headers='Location: /')

    # Envia pagina resetada
    # Adiciona cartas do banco de dados ao html
    notes_li = []
    for dados in sql_entity.get_all():
        notes_li.append(
            load_template('components/note.html').format(title=dados.title, details=dados.content,id=dados.id))
    notes = '\n'.join(notes_li)
    sql_entity.close()
    return build_response(load_template('index.html').format(notes=notes))

# Tela Edit
def edit(request, id_note):
    # Carrega Dados Cartao
    sql_entity = database.Database('data/banco')
    dado = sql_entity.get_id(id_note)
    note = load_template('components/note_edit.html').format(title=dado.title, details=dado.content, id=dado.id)

    # GET → mostra tela de edição
    if request.startswith('GET'):
        note = load_template('components/note_edit.html').format(title=dado.title, details=dado.content, id=dado.id)
        return build_response(load_template('edit.html').format(note=note))

    # POST → trata o botão pressionado
    if request.startswith('POST'):
        params = extrair_params(request)

        if params['acao'] == 'salvar':
            note = sql_entity.get_id(id_note)
            note.title = params['titulo']
            note.content = params['detalhes']
            sql_entity.update(note)

        elif params['acao'] == 'cancelar':
            pass

        # Volta para a tela principal
        sql_entity.close()
        #return index(request)
        return build_response(code=303, reason='See Other', headers='Location: /' )

def notfound():
    return build_response(
        body=load_template('404.html'),
        code=404,
        reason='Not Found'
    )