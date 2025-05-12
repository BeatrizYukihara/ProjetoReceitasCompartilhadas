from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
from dao.cardapio_dao import CardapioDAO

# Criar instância do DAO
usuario_dao = UsuarioDAO()
cardapio_dao = CardapioDAO()

# Criar objeto Usuario (id=None porque é autoincrementado no banco)
usuario_teste = Usuario(None, 'João Teste', 'joao@teste.com', '1234', None)

cardapio_dao.adicionar_receita_cardapio(1, "Segunda Feira", "Jantar", 1)
# Inserir no banco
usuario_dao.inserir(usuario_teste)

print("Usuário de teste criado com sucesso!")
