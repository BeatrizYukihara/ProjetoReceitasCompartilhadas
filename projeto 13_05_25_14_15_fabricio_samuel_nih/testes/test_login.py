import pytest
from app import app as flask_app
from flask import session
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.secret_key = 'teste'
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_index_redirects_to_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

def test_get_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'<form' in response.data  # verifica se tem um formulário no HTML

@patch('app.UsuarioDAO')
@patch('app.bcrypt.checkpw')
def test_login_post_valid_credentials(mock_checkpw, mock_usuario_dao, client):
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.nome = 'Teste'
    mock_user.senha = b'hashed_password'
    mock_usuario_dao.return_value.buscar_por_email_login.return_value = mock_user
    mock_checkpw.return_value = True

    response = client.post('/login', data={'email': 'teste@example.com', 'senha': '1234'}, follow_redirects=False)

    assert response.status_code == 302
    assert '/minhas_receitas' in response.headers['Location']

@patch('app.UsuarioDAO')
@patch('app.bcrypt.checkpw')
def test_login_post_invalid_credentials(mock_checkpw, mock_usuario_dao, client):
    mock_user = MagicMock()
    mock_user.senha = b'hashed_password'
    mock_usuario_dao.return_value.buscar_por_email_login.return_value = mock_user
    mock_checkpw.return_value = False

    response = client.post('/login', data={'email': 'teste@example.com', 'senha': 'errada'}, follow_redirects=False)

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

@patch('app.usuario_dao')
def test_cadastro_post_email_existente(mock_usuario_dao, client):
    mock_usuario_dao.buscar_por_email.return_value = True

    response = client.post('/cadastro', data={
        'nome': 'Nome',
        'email': 'ja@existe.com',
        'senha': '1234'
    })

    assert response.status_code == 400
    assert 'Email já cadastrado' in response.data.decode('utf-8')

@patch('app.usuario_dao')
def test_cadastro_post_valido(mock_usuario_dao, client):
    mock_usuario_dao.buscar_por_email.return_value = False

    response = client.post('/cadastro', data={
        'nome': 'Novo',
        'email': 'novo@example.com',
        'senha': '1234'
    })

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

def test_logout_clears_session(client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1
        sess['usuario_nome'] = 'Teste'

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/login')

    with client.session_transaction() as sess:
        assert 'usuario_id' not in sess
        assert 'usuario_nome' not in sess
