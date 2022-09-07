from utils import build_response, load_template, Database, Note

def index(request):

    note_template = load_template('components/note.html')

    db = Database('banco')
    code = 200
    reason = 'OK'
    headers = ''

    dados = db.get_all()
    
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
            
        if corpo.startswith('id-delete'):
            db.delete(params['id-delete'])
        
        elif corpo.startswith('title'):
            db.add(Note(title=params['title'], content=params['content']))

        elif corpo.startswith('id-update'):
            if not params['title'] or not params['content']:
                None
            else:
                db.update(Note(id=int(params['id-update']), title=params['title'], content=params['content']))
            
        code = 303
        reason = 'See Other'
        headers = 'Location: /'

    # Gerando o HTML das notas
    notes_li = [
        note_template.format(id=dado.id, title=dado.title, content=dado.content)
        for dado in dados
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