# Representa a entidade Cardapio com os dados do banco
class Cardapio:
    def __init__(self, id, id_refeicoes_cardapio, id_usuario ):
        self.id = id
        self.id_refeicoes_cardapio = id_refeicoes_cardapio 
        self.id_usuario = id_usuario

class Refeicoes_Cardapio:
    def __init__(self, id, dia_semana, tipo, id_receita ):
        self.id = id
        self.dia_semana = dia_semana
        self.tipo = tipo
        self.id_receita = id_receita
