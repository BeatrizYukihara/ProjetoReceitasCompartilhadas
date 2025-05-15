import pytest
from unittest.mock import patch, MagicMock
from app import app as flask_app
from app import usuario_dao  # vamos mockar essa instância

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.secret_key = 'teste'  # para sessões e flash
    with flask_app.test_client() as client:
        yield client


def test_index_redireciona_para_login(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.location


def test_login_get_retorna_template(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


@patch('app.bcrypt')
def test_login_post_credenciais_corretas(mock_bcrypt, client):
    usuario_mock = MagicMock()
    usuario_mock.id = 1
    usuario_mock.nome = 'Maria'
    usuario_mock.senha = '$2b$12$fakehash'  # string simulando um hash

    with patch.object(usuario_dao, 'buscar_por_email_login', return_value=usuario_mock):
        mock_bcrypt.checkpw.return_value = True  # simula senha correta

        response = client.post('/login', data={
            'email': 'maria@email.com',
            'senha': 'senha123'
        })

        assert response.status_code == 302
        assert '/minhas_receitas' in response.location



@patch('app.bcrypt')
def test_login_post_credenciais_invalidas(mock_bcrypt, client):
    with patch.object(usuario_dao, 'buscar_por_email_login', return_value=None):
        response = client.post('/login', data={
            'email': 'naoexiste@email.com',
            'senha': 'errada'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Login inv\xc3\xa1lido' in response.data


def test_logout_limpa_sessao(client):
    with client.session_transaction() as sess:
        sess['usuario_id'] = 1
        sess['usuario_nome'] = 'Maria'

    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302
    assert '/login' in response.location
