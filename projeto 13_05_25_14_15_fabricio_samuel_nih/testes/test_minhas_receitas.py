import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


# -------------------- /api/receitas (POST) --------------------

@patch('app.receita_dao')
def test_api_adicionar_receita_autenticado(mock_receita_dao, client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1

    dados = {
        'titulo': 'Bolo',
        'porcoes': 8,
        'tempoPreparo': '40 minutos',
        'tipo': 'Doce',
        'ingredientes': [
            {'produto': 'Farinha', 'quantidade': 2.0, 'unidade': 'xícaras'},
        ],
        'modoPreparo': ['Misturar tudo', 'Assar por 40 minutos']
    }

    response = client.post('/api/receitas', json=dados)
    assert response.status_code == 200
    assert response.get_json() == {'mensagem': 'Receita adicionada com sucesso'}
    assert mock_receita_dao.inserir.called is True

def test_api_adicionar_receita_nao_autenticado(client):
    response = client.post('/api/receitas', json={})
    assert response.status_code == 401
    assert response.get_json() == {'erro': 'Não autenticado'}

# -------------------- /api/receitas/<id> (DELETE) --------------------

@patch('app.receita_dao')
def test_api_excluir_receita_autenticado(mock_receita_dao, client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1

    response = client.delete('/api/receitas/10')
    assert response.status_code == 200
    assert response.get_json() == {'mensagem': 'Receita excluída com sucesso'}
    mock_receita_dao.excluir.assert_called_once_with(10)

def test_api_excluir_receita_nao_autenticado(client):
    response = client.delete('/api/receitas/10')
    assert response.status_code == 401
    assert response.get_json() == {'erro': 'Não autenticado'}
