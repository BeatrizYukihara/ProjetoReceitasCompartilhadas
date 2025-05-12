import sqlite3
from models.cardapio import Cardapio, Refeicoes_Cardapio

class CardapioDAO:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def adicionar_ao_cardapio(self, dados):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Refeicoes_Cardapio (dia_semana, tipo, id_receita)
            VALUES (?, ?, ?)
        """, (dados['dia'], dados['refeicao'], dados['receita_id']))
        id_refeicao = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Cardapio (refeicoes_Cardapio_FK, id_usuario_FK)
            VALUES (?, ?)
        """, (id_refeicao, dados['usuario_id']))
        conn.commit()
        conn.close()
        return True

    def remover_do_cardapio(self, dados):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM Cardapio
            WHERE id_usuario_FK = ? AND refeicoes_Cardapio_FK IN (
                SELECT id FROM Refeicoes_Cardapio
                WHERE dia_semana = ? AND tipo = ? AND id_receita = ?
            )
        """, (dados['usuario_id'], dados['dia'], dados['refeicao'], dados['receita_id']))
        conn.commit()
        conn.close()
        return True

    def visualizar_receitas_cardapio(self, usuario_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rc.id as rc_id, rc.dia_semana, rc.tipo, rc.id_receita,
                   c.id as c_id, c.id_usuario_FK
            FROM Cardapio c
            JOIN Refeicoes_Cardapio rc ON rc.id = c.refeicoes_Cardapio_FK
            WHERE c.id_usuario_FK = ?
        """, (usuario_id,))
        dados = cursor.fetchall()
        conn.close()

        resultado = {dia: {'Café da Manhã': [], 'Almoço': [], 'Jantar': []} for dia in
                     ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']}

        for row in dados:
            refeicao = Refeicoes_Cardapio(row['rc_id'], row['dia_semana'], row['tipo'], row['id_receita'])
            resultado[refeicao.dia_semana][refeicao.tipo].append(str(refeicao.id_receita))

        return resultado
