import sqlite3
from models.cardapio import Cardapio, Refeicoes_Cardapio

class CardapioDAO:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def adicionar_receita_cardapio(self, usuario_id, dia_semana, tipo, receita_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Inserir a refeição no cardápio
        cursor.execute("""
            INSERT INTO Refeicoes_Cardapio (dia_semana, tipo, id_receita_FK)
            VALUES (?, ?, ?)
        """, (dia_semana, tipo, receita_id))
        
        refeicao_id = cursor.lastrowid  # pega o ID gerado para essa refeição

        # Relacionar a refeição com o usuário na tabela Cardapio
        cursor.execute("""
            INSERT INTO Cardapio (refeicoes_Cardapio_FK, id_usuario_FK)
            VALUES (?, ?)
        """, (refeicao_id, usuario_id))

        conn.commit()
        conn.close()

    def excluir_receita_cardapio(self, usuario_id, dia_semana, tipo, receita_id):
        """Exclui uma receita do cardápio do usuário para o dia e tipo especificado, utilizando o ID da receita."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Verificar se a receita está associada ao usuário
        cursor.execute("""
            SELECT 1 FROM usuario_receita
            WHERE usuario_id = ? AND receita_id = ?
        """, (usuario_id, receita_id))
        
        if cursor.fetchone():
            # Excluir a receita do cardápio para o dia e tipo especificado
            cursor.execute("""
                DELETE FROM Refeicoes_Cardapio 
                WHERE dia_semana = ? AND tipo = ? AND id_receita = ?
            """, (dia_semana, tipo, receita_id))
            conn.commit()
        conn.close()

    def visualizar_receitas_cardapio(self, usuario_id):
        """Retorna todas as receitas associadas ao cardápio de um usuário, organizadas por dia e tipo."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Buscar todas as receitas associadas ao cardápio do usuário
        cursor.execute("""
            SELECT rc.dia_semana, rc.tipo, r.id, r.nome
            FROM Refeicoes_Cardapio rc
            INNER JOIN Receita r ON rc.id_receita = r.id
            INNER JOIN usuario_receita ur ON r.id = ur.receita_id
            WHERE ur.usuario_id = ?
        """, (usuario_id,))
        
        receitas = cursor.fetchall()
        conn.close()
        
        # Organizar as receitas por dia e tipo
        cardapio = {}
        for dia, tipo, receita_id, nome in receitas:
            if dia not in cardapio:
                cardapio[dia] = {}
            if tipo not in cardapio[dia]:
                cardapio[dia][tipo] = []
            cardapio[dia][tipo].append({'id': receita_id, 'nome': nome})
        
        return cardapio
