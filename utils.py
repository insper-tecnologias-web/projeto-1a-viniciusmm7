import sqlite3
from dataclasses import dataclass

# ========= Classe das notas =========
@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

# ========= Classe do banco de dados =========
# ----- Atualmente somente para notas
class Database:
    def __init__(self, name:str):
        self.conn = sqlite3.connect(f'{name}.db')
        c = self.conn.cursor()
        c.execute('pragma encoding=UTF8')
        rows = c.fetchall()
        self.conn.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL);")

    def add(self, note:Note):
        self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}');")
        self.conn.commit()

    get_all = lambda self: [Note(id=linha[0], title=linha[1], content=linha[2]) for linha in self.conn.execute("SELECT id, title, content FROM note;")]

    def update(self, entry:Note):
        self.conn.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id};")
        self.conn.commit()

    def delete(self, note_id:int):
        self.conn.execute(f"DELETE FROM note WHERE id = {note_id};")
        self.conn.commit()

# ========= Funcoes auxiliares =========
def extract_route(req):
    try:
        return req.split()[1].replace('/', '', 1)
    except:
        return ''

def read_file(path):
    with open(path, 'r+b') as f:
        file = f.read()
        f.close()
    return file

def load_template(html_file):
    with open(f'./templates/{html_file}', encoding='utf8') as f:
        template = f.read()
        f.close()
    return template

def build_response(body='', code=200, reason='OK', headers=''):
    if headers != '':
        return f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'.encode()
    return f'HTTP/1.1 {code} {reason}\n\n{body}'.encode()