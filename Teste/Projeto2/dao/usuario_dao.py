import sqlite3
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def buscar_por_email(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return Usuario(*row) if row else None

    def buscar_por_id(self, usuario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE id = ?", (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        return Usuario(*row) if row else None

    def inserir(self, usuario):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuario (nome, email, senha)
            VALUES (?, ?, ?)
        """, (usuario.nome, usuario.email, usuario.senha))
        conn.commit()
        conn.close()

    def excluir(self, usuario_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuario WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()

    def atualizar(self, usuario_id, nome, email, telefone, prato, foto):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE usuarios
            SET nome = ?, email = ?, telefone = ?, prato_favorito = ?, foto = ?
            WHERE id = ?
        ''', (nome, email, telefone, prato, foto, usuario_id))
        self.conn.commit()




