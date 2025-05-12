# Representa a entidade Usuario com os dados do banco
class Usuario:
    def __init__(self, id, nome, email, senha, prato_favorito=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.prato_favorito = prato_favorito
