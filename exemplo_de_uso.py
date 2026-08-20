from database import Database
from database import Note
import json

db = Database('banco')

def load_data(name):
    return json.load(open(f'data/{name}', encoding='utf-8'))  

for note in load_data('notes.json'):
    db.add(Note(title=note['titulo'], content=note['detalhes']))

#db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
#db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')