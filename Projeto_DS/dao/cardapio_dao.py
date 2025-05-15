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
            INSERT INTO Refeicoes_Cardapio (dia_semana, tipo, id_receita_FK) 
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
        try:
            # Buscar id da Refeição
            cursor.execute("""
                SELECT id FROM Refeicoes_Cardapio
                WHERE dia_semana = ? AND tipo = ? AND id_receita_FK = ?
            """, (dados['dia'], dados['refeicao'], dados['receita_id']))
            resultado = cursor.fetchone()

            if not resultado:
                print("Nenhuma refeição encontrada para exclusão:", dados)
                return False

            id_refeicao = resultado[0]

            cursor.execute("""
                DELETE FROM Cardapio
                WHERE id_usuario_FK = ? AND refeicoes_Cardapio_FK = ?
            """, (dados['usuario_id'], id_refeicao))

            cursor.execute("""
                DELETE FROM Refeicoes_Cardapio
                WHERE id = ?
            """, (id_refeicao,))

            conn.commit()
            print("Delete realizado com sucesso")
            return True
        finally:
            conn.close()






    def visualizar_receitas_cardapio(self, usuario_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rc.dia_semana, rc.tipo, rc.id_receita_FK, r.nome
            FROM Cardapio c
            JOIN Refeicoes_Cardapio rc ON c.refeicoes_Cardapio_FK = rc.id
            JOIN Receita r ON r.id = rc.id_receita_FK
            WHERE c.id_usuario_FK = ?
        """, (usuario_id,))
        
        dados = cursor.fetchall()
        conn.close()

        resultado = {dia: {'Café da Manhã': [], 'Almoço': [], 'Jantar': []} for dia in
                    ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']}

        for row in dados:
            dia_semana = row["dia_semana"]
            tipo_refeicao = row["tipo"]
            id_receita = row["id_receita_FK"]
            nome_receita = row["nome"]

            if dia_semana in resultado and tipo_refeicao in resultado[dia_semana]:
                resultado[dia_semana][tipo_refeicao].append({'id': id_receita, 'nome': nome_receita})

        return resultado




