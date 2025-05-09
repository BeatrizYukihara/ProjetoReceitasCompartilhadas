from flask import (
    Flask, render_template, request,
    redirect, url_for, session, jsonify
)

from models.receita import Receita, Preparos, Ingrediente
from models.usuario import Usuario
from models.cardapio import Cardapio, Refeicoes_Cardapio
from dao.receita_dao import ReceitaDAO
from dao.usuario_dao import UsuarioDAO
from dao.cardapio_dao import CardapioDAO

print("Iniciando o aplicativo Flask...")
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
usuario_dao = UsuarioDAO()
receita_dao = ReceitaDAO()
cardapio_dao = CardapioDAO()


#=======================================ROTAS LOGIN===========================================
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = usuario_dao.buscar_por_email(email)
        if usuario and usuario.senha == senha:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return redirect(url_for('minhas_receitas', id_usuario=usuario.id, nome_usuario = usuario.nome))
        return "Login inválido", 401
    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        if usuario_dao.buscar_por_email(email):
            return "Email já cadastrado", 400
        novo_usuario = Usuario(None, nome, email, senha)
        usuario_dao.inserir(novo_usuario)
        return redirect(url_for('login'))
    return render_template('cadastro.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))





#=======================================ROTAS MINHAS RECEITAS===========================================

@app.route('/minhas_receitas')
def minhas_receitas():
    id_usuario = session['usuario_id']  
    nome_usuario = session['usuario_nome']
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('minhas_receitas.html', nome_usuario=nome_usuario, id_usuario=id_usuario)



@app.route('/api/receitas', methods=['POST'])
def api_adicionar_receita():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    dados = request.json
    usuario_id = session['usuario_id']
    receita = Receita(None, dados['titulo'], dados['porcoes'], dados['tempoPreparo'], dados['tipo'], None)
    ingredientes = [
        Ingrediente(None, i['produto'], float(i['quantidade']), i['unidade'], None)
        for i in dados['ingredientes']
    ]

    preparos = [
        Preparos(None, idx + 1, passo, None)
        for idx, passo in enumerate(dados['modoPreparo'])
    ]

    receita_dao.inserir(receita, ingredientes, preparos, usuario_id)

    return jsonify({'mensagem': 'Receita adicionada com sucesso'})


@app.route('/api/receitas/<int:receita_id>', methods=['DELETE'])
def api_excluir_receita(receita_id):
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401

    receita_dao.excluir(receita_id)
    return jsonify({'mensagem': 'Receita excluída com sucesso'})

#=======================================ROTAS PRECIFICAR===========================================

@app.route('/precificar')
def precificacao():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('precificar.html', nome_usuario=session['usuario_nome'])

@app.route('/atualizar_preco', methods=['POST'])
def atualizar_preco():
    data = request.json
    receita_id = data['receita_id']
    preco_total = data['preco_total']

    receita_dao.atualizar_preco(preco_total, receita_id)
    return jsonify({'status': 'sucesso', 'preco': preco_total})



##=======================================ROTAS CARDAPIO===========================================
@app.route('/cardapio')
def cardapio():
    id_usuario = session['usuario_id']  
    nome_usuario = session['usuario_nome']
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('cardapio.html', nome_usuario=nome_usuario, id_usuario=id_usuario)

# Rota para adicionar uma receita ao cardápio
@app.route('/cardapio/adicionar', methods=['POST'])
def adicionar_receita_cardapio():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    dados = request.json
    usuario_id = session['usuario_id']
    dia_semana = session['dia_semana']
    tipo = session['tipo']
    receita_id = session['receita_id']

    cardapio_dao.adicionar_receita_cardapio(usuario_id, dia_semana, tipo, receita_id)
    return jsonify({'mensagem': 'Receita adicionada ao cardápio com sucesso'}), 200

@app.route('/cardapio/preparar', methods=['POST'])
def preparar_dados_cardapio():
    if 'usuario_id' not in session:
        return jsonify({'sucesso': False, 'erro': 'Usuário não autenticado'}), 401
    dados = request.json
    receita_id = dados.get('receita_id')
    dia = dados.get('dia')
    tipo = dados.get('refeicao')
    if not all([receita_id, dia, tipo]):
        return jsonify({'sucesso': False, 'erro': 'Dados incompletos'}), 400
    session['receita_id'] = receita_id
    session['dia_semana'] = dia
    session['tipo'] = tipo
    return jsonify({'sucesso': True, 'mensagem': 'Dados armazenados na sessão com sucesso'})


# Rota para excluir uma receita do cardápio
@app.route('/api/cardapio/excluir', methods=['POST'])
def excluir_receita_cardapio():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    dados = request.json
    usuario_id = session['usuario_id']
    dia_semana = dados.get('dia_semana')
    tipo = dados.get('tipo')
    receita_id = dados.get('receita_id')

    if not all([dia_semana, tipo, receita_id]):
        return jsonify({'erro': 'Dados incompletos'}), 400

    cardapio_dao.excluir_receita_cardapio(usuario_id, dia_semana, tipo, receita_id)
    return jsonify({'mensagem': 'Receita removida do cardápio com sucesso'}), 200


# Rota para visualizar o cardápio do usuário logado
@app.route('/api/cardapio', methods=['GET'])
def visualizar_cardapio():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    usuario_id = session['usuario_id']
    cardapio = cardapio_dao.visualizar_receitas_cardapio(usuario_id)
    return jsonify(cardapio), 200

#=======================================ROTAS MEU PERFIL===========================================

@app.route('/meu_perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('meu_perfil.html', nome_usuario=session['usuario_nome'])


@app.route('/atualizar_usuario', methods=['POST'])
def atualizar_usuario():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401

    data = request.json
    usuario_id = session['usuario_id']
    nome = data.get('nome')
    email = data.get('email')
    telefone = data.get('telefone')
    prato = data.get('prato')
    foto = data.get('foto')

    usuario_dao.atualizar(usuario_id, nome, email, telefone, prato, foto)
    session['usuario_nome'] = nome 

    return jsonify({'status': 'sucesso'})


@app.route('/excluir_conta', methods=['POST'])
def excluir_conta():
    data = request.json
    usuario_id = data.get('usuario_id')

    usuario_dao.excluir(usuario_id)
    return jsonify({'status': 'conta excluída'})

#===================================API´S (BUSCAR INFOS NO BD)==========================================
@app.route('/api/receitas', methods=['GET'])
def api_listar_receitas():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401

    usuario_id = session['usuario_id']
    receitas = receita_dao.listar_por_usuario(usuario_id)

    receitas_json = []
    for r in receitas:
        receita = r['receita']
        ingredientes = r['ingredientes']
        preparos = r['preparos']

        receitas_json.append({
            'id': receita.id,
            'titulo': receita.nome,
            'tipo': receita.tipo,
            'preco': receita.preco,
            'tempoPreparo': receita.tempo_preparo,  
            'porcoes': receita.porcao,              
            'ingredientes': [{
                'produto': ing.nome,
                'quantidade': ing.quantidade,
                'unidade': ing.unidade
            } for ing in ingredientes],
            'modoPreparo': [prep.descricao for prep in sorted(preparos, key=lambda p: p.etapa)]
        })
            
    return jsonify(receitas_json)


@app.route('/api/usuario/<int:usuario_id>', methods=['GET'])
def buscar_usuario_por_id(usuario_id):
    usuario = usuario_dao.buscar_por_id(usuario_id)
    if usuario:
        return jsonify({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'foto': usuario.foto
        })
    else:
        return jsonify({'erro': 'Usuário não encontrado'}), 404




if __name__ == '__main__':
    app.run(debug=True)
