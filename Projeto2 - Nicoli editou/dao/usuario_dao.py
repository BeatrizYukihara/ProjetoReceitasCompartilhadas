import sqlite3
import bcrypt
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path


    def autenticar_usuario(email, senha, UsuarioDAO):
        try:
            # Busca o usuário pelo email usando a função da classe UsuarioDAO
            usuario_bd = UsuarioDAO().buscar_por_email(email)

            if usuario_bd:
                # A senha armazenada no banco está em formato hash, então comparamos com a senha informada
                senha_armazenada = usuario_bd.senha.encode('utf-8')  # Certifique-se de que a senha está em bytes

                # Verifica se a senha inserida corresponde ao hash armazenado
                if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada):
                    # Se a senha for válida, retorna o objeto Usuario com as informações do banco
                    return Usuario(
                        id=usuario_bd.id,
                        nome=usuario_bd.nome,
                        email=usuario_bd.email,
                        senha=usuario_bd.senha,  # Aqui ainda armazenamos o hash
                        tipo_usuario=usuario_bd.tipo_usuario,
                        telefone=usuario_bd.telefone,
                        especialidade=usuario_bd.especialidade,
                        crm=usuario_bd.crm
                    )
            return None  # Se o usuário não for encontrado ou a senha não corresponder

        except Exception as e:
            print(f"Erro ao autenticar o usuário: {e}")
            return None

    def email_existe(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM Usuario WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        conn.close()
        return True if resultado else False
    
    def buscar_por_email_login(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Retorna todos os dados da linha, incluindo o ID
            return Usuario(id=row[0], nome=row[1], email=row[2], senha=row[3])
        return None

    
    def buscar_por_email(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Usuario(*row)  # Passa todos os valores de uma vez para o construtor
        return None


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

    def atualizar(self, usuario_id, nome, email, prato):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Usuario
            SET nome = ?, email = ?, prato_favorito = ?
            WHERE id = ?
        ''', (nome, email, prato, usuario_id))
        conn.commit()
        conn.close()

    def contar_receitas_do_usuario(self, usuario_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuario_receita WHERE usuario_id = ?", (usuario_id,))
            resultado = cursor.fetchone()
            conn.close()
            return resultado[0] if resultado else 0
        except Exception as e:
            print(f"Erro ao contar receitas do usuário: {e}")
            return 0