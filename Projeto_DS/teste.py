from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
from dao.cardapio_dao import CardapioDAO
from flask import (
    Flask, render_template, request,flash,
    redirect, url_for, session, jsonify
)
import bcrypt
from models.receita import Receita, Preparos, Ingrediente
from models.usuario import Usuario
from models.cardapio import Cardapio, Refeicoes_Cardapio
from dao.receita_dao import ReceitaDAO
from dao.usuario_dao import UsuarioDAO
from dao.cardapio_dao import CardapioDAO


# Criar instância do DAO
usuario_dao = UsuarioDAO()
cardapio_dao = CardapioDAO()


dados = ({
        'dia': "Segunda",
        'refeicao': "Almoço",
        'receita_id': 1,
        'usuario_id': 1
    })

conn = 'database.db'.get_connection()
cursor = conn.cursor()
# Primeiro localiza o id da Refeicao
cursor.execute("""
            SELECT id FROM Refeicoes_Cardapio
            WHERE dia_semana = ? AND tipo = ? AND id_receita_FK = ?
        """, (dados['dia'], dados['refeicao'], dados['receita_id']))

resultado = cursor.fetchone()
if resultado:
        id_refeicao = resultado[0]

# Remove somente do Cardápio do usuário atual
cursor.execute("""
                DELETE FROM Cardapio
                WHERE id_usuario_FK = ? AND refeicoes_Cardapio_FK = ?
            """, (dados['usuario_id'], id_refeicao))
conn.commit()
conn.close()
