# Representa a entidade Receita com os dados do banco
class Receita:
    def __init__(self, id, nome, porcao, tempo_preparo, tipo, preco):
        self.id = id
        self.nome = nome
        self.porcao = porcao
        self.tempo_preparo = tempo_preparo
        self.tipo = tipo
        self.preco = preco

class Preparos:
    def __init__(self, id, etapa, descricao, id_receita):
        self.id = id
        self.etapa = etapa
        self.descricao = descricao
        self.id_receita = id_receita

class Ingrediente:
    def __init__(self, id, nome, quantidade, unidade, id_receita_FK):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.unidade = unidade
        self.id_receita_FK = id_receita_FK

