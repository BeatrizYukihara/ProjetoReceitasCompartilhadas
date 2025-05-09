# Representa a entidade Usuario com os dados do banco
class Usuario:
    def __init__(self, id, nome, email, senha, foto):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.foto = foto
