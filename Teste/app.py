from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('meu_banco.db')
    conn.row_factory = sqlite3.Row  # Retorna dados como dicionário
    return conn

@app.route('/')
def index():
    return render_template('precificar.html')

@app.route('/get_receitas/<int:usuario_id>', methods=['GET'])
def get_receitas(usuario_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM receitas WHERE usuario_id = ?', (usuario_id,))
    receitas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(receitas)

@app.route('/get_ingredientes/<int:receita_id>', methods=['GET'])
def get_ingredientes(receita_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ingredientes WHERE receita_id = ?', (receita_id,))
    ingredientes = [dict(row) for row in cursor.fetchall()]
    print(ingredientes)
    conn.close()
    return jsonify(ingredientes)

@app.route('/atualizar_preco', methods=['POST'])
def atualizar_preco():
    data = request.json
    receita_id = data['receita_id']
    preco_total = data['preco_total']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE receitas SET preco = ? WHERE id = ?', (preco_total, receita_id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'sucesso', 'preco': preco_total})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
