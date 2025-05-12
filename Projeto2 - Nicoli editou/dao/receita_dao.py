import sqlite3
from models.receita import Receita, Preparos, Ingrediente

class ReceitaDAO:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def listar_por_usuario(self, usuario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.id, r.nome, r.porcao, r.tempo_preparo, r.tipo, r.preco
            FROM receita r
            INNER JOIN usuario_receita ur ON r.id = ur.receita_id
            WHERE ur.usuario_id = ?
        """, (usuario_id,))
        receitas_rows = cursor.fetchall()

        receitas_completas = []

        for row in receitas_rows:
            receita = Receita(*row)

            # Ingredientes
            cursor.execute("SELECT * FROM Ingredientes WHERE id_receita_FK = ?", (receita.id,))
            ingredientes_rows = cursor.fetchall()
            ingredientes = [Ingrediente(*ing) for ing in ingredientes_rows]

            # Preparos
            cursor.execute("SELECT * FROM Preparos WHERE id_receita_FK = ?", (receita.id,))
            preparos_rows = cursor.fetchall()
            preparos = [Preparos(*p) for p in preparos_rows]

            receitas_completas.append({
                'receita': receita,
                'ingredientes': ingredientes,
                'preparos': preparos
            })

        conn.close()
        return receitas_completas


    def inserir(self, receita, ingredientes, preparos, usuario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Receita (nome, porcao, tempo_preparo, tipo, preco)
            VALUES (?, ?, ?, ?, ?)
        """, (receita.nome, receita.porcao, receita.tempo_preparo, receita.tipo, receita.preco))
        receita_id = cursor.lastrowid
        # Relacionar com o usuário
        cursor.execute("INSERT INTO usuario_receita (usuario_id, receita_id) VALUES (?, ?)",
                    (usuario_id, receita_id))
        # Inserir ingredientes
        for ing in ingredientes:
            cursor.execute("""
                INSERT INTO Ingredientes (nome, quantidade, unidade, id_receita_FK)
                VALUES (?, ?, ?, ?)
            """, (ing.nome, ing.quantidade, ing.unidade, receita_id))
        # Inserir preparos
        for prep in preparos:
            cursor.execute("""
                INSERT INTO Preparos (etapa, descricao, id_receita_FK)
                VALUES (?, ?, ?)
            """, (prep.etapa, prep.descricao, receita_id))
        conn.commit()
        conn.close()


    def excluir(self, receita_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Ingredientes WHERE id_receita_FK = ?", (receita_id,))
        cursor.execute("DELETE FROM Preparos WHERE id_receita_FK = ?", (receita_id,))
        cursor.execute("DELETE FROM usuario_receita WHERE receita_id = ?", (receita_id,))
        cursor.execute("DELETE FROM Receita WHERE id = ?", (receita_id,))
        conn.commit()
        conn.close()

    def atualizar_preco(self, preco, id_receita):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Receita
            SET preco = ?
            WHERE id = ?
        """, (preco, id_receita))
        conn.commit()
        conn.close()