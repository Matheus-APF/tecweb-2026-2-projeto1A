import sqlite3
class Database:
    def __init__(self, nome_banco):
        self.conn = sqlite3.connect(nome_banco + '.db')
        self.table = self.conn.execute("CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL UNIQUE);")

    def add(self, note):
        self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}');")
        self.conn.commit()

    def get_all(self):
        notes = []
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            notes.append(Note(id=int(id), title=title, content=content))
        return notes

    def update(self, entry):
        self.conn.execute(f"UPDATE note SET title = '{entry.title}' WHERE id = {entry.id}")
        self.conn.execute(f"UPDATE note SET content = '{entry.content}' WHERE id = {entry.id}")

    def delete(self, note_id):
        self.conn.execute(f"DELETE FROM note WHERE id = {note_id}")
        self.conn.commit()

from dataclasses import dataclass
@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''