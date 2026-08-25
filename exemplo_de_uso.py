from database import Database, Note
import json


def load_data(name):
    return json.load(open(f'data/{name}', encoding='utf-8'))


def adicionar_coluna_favorite(db):
    """Adiciona a coluna favorite caso ela ainda não exista."""

    cursor = db.conn.execute("PRAGMA table_info(note)")
    colunas = [linha[1] for linha in cursor]

    if 'favorite' not in colunas:
        db.conn.execute("""
            ALTER TABLE note
            ADD COLUMN favorite INTEGER NOT NULL DEFAULT 0
        """)
        db.conn.commit()
        print('Coluna favorite adicionada.')
    else:
        print('A coluna favorite já existe.')


db = Database('banco')

# Atualiza a estrutura do banco já existente
adicionar_coluna_favorite(db)

# Adiciona as anotações do JSON
for note in load_data('notes.json'):
    db.add(
        Note(
            title=note['titulo'],
            content=note['detalhes']
        )
    )

# Exibe as anotações
notes = db.get_all()

for note in notes:
    print(
        f'Anotação {note.id}:\n'
        f'  Título: {note.title}\n'
        f'  Conteúdo: {note.content}\n'
        f'  Favorita: {bool(note.favorite)}\n'
    )

db.close()