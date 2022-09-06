from utils import build_response, load_template, Database, Note

def index(request):
    db = Database('banco')
    code = 200
    reason = 'OK'
    headers = ''
    if request.startswith('POST'):
        request = request.replace('\r', '')

        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}

        for chave_valor in corpo.split('&'):
            itens = chave_valor.split('=')
            chave = itens[0]
            valor = ' '.join(itens[1].split('+'))
            params[chave] = valor
            
        db.add(Note(title=params['title'], content=params['content']))
        code = 303
        reason = 'See Other'
        headers = 'Location: /'

    # Gerando o HTML das notas
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, content=dados.content)
        for dados in db.get_all()
    ]
    notes = '\n'.join(notes_li)

    return build_response(
        code=code,
        reason=reason,
        headers=headers,
        body=load_template('index.html').format(
            notes=notes
        )
    )