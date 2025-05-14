import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app

#=======================================TESTE CADASTRO===========================================

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


@patch('app.usuario_dao')
@patch('app.Usuario')
def test_cadastrar_usuario_sucesso(mock_usuario_class, mock_usuario_dao, client):
    mock_usuario_dao.email_existe.return_value = False
    mock_usuario_dao.inserir.return_value = None

    response = client.post('/cadastrar_usuario', data={
        'nome': 'Maria',
        'email': 'maria@email.com',
        'senha': 'senha123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data  # Verifica se redirecionou para a página de login


@patch('app.usuario_dao')
def test_cadastrar_usuario_email_ja_existente(mock_usuario_dao, client):
    mock_usuario_dao.email_existe.return_value = True

    response = client.post('/cadastrar_usuario', data={
        'nome': 'João',
        'email': 'joao@email.com',
        'senha': 'senha123'
    })

    assert response.status_code == 200
    assert b'Email j\xc3\xa1 est\xc3\xa1 cadastrado.' in response.data


@patch('app.usuario_dao')
@patch('app.Usuario')
def test_cadastrar_usuario_erro_insercao(mock_usuario_class, mock_usuario_dao, client):
    mock_usuario_dao.email_existe.return_value = False
    mock_usuario_dao.inserir.side_effect = Exception("Erro de banco")

    response = client.post('/cadastrar_usuario', data={
        'nome': 'Ana',
        'email': 'ana@email.com',
        'senha': 'senha123'
    })

    assert response.status_code == 200
    assert b'Ocorreu um erro ao cadastrar o paciente' in response.data
