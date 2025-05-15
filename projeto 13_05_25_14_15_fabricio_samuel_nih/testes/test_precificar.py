import pytest
from unittest.mock import patch
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_precificar_redireciona_para_login_se_nao_autenticado(client):
    # Garante que a sessão está limpa
    with client.session_transaction() as session:
        session.clear()

    response = client.get('/precificar', follow_redirects=True)

    # Redireciona para a página de login
    assert response.status_code == 200
    assert 'Login' in response.get_data(as_text=True)


def test_precificar_retorna_pagina_se_autenticado(client):
    # Simula sessão de usuário autenticado
    with client.session_transaction() as session:
        session['usuario_id'] = 1
        session['usuario_nome'] = 'Maria'

    response = client.get('/precificar')

    assert response.status_code == 200
    assert 'Maria' in response.get_data(as_text=True)
    assert 'Precificar' in response.get_data(as_text=True)  # ou o título da página, se existir


@patch('app.receita_dao.atualizar_preco')  # Substitui o método do DAO por um mock
def test_atualizar_preco_funciona(mock_atualizar_preco, client):
    mock_atualizar_preco.return_value = None  # Simula execução bem-sucedida

    data = {
        'receita_id': 1,
        'preco_total': 45.75
    }

    response = client.post('/atualizar_preco', json=data)

    # Verifica se a função foi chamada corretamente
    mock_atualizar_preco.assert_called_once_with(45.75, 1)

    # Verifica resposta JSON
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'sucesso'
    assert json_data['preco'] == 45.75
