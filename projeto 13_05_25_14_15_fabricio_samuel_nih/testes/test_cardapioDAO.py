import unittest
from unittest.mock import MagicMock, patch
from dao.cardapio_dao import CardapioDAO

class TestCardapioDAO(unittest.TestCase):

    @patch('dao.cardapio_dao.sqlite3.connect')
    def test_adicionar_ao_cardapio(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1

        dao = CardapioDAO("fake_path.db")
        dados = {'dia': 'Segunda', 'refeicao': 'Almoço', 'receita_id': 1, 'usuario_id': 10}
        result = dao.adicionar_ao_cardapio(dados)

        self.assertTrue(result)
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('dao.cardapio_dao.sqlite3.connect')
    def test_remover_do_cardapio(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        dao = CardapioDAO("fake_path.db")
        dados = {'dia': 'Terça', 'refeicao': 'Jantar', 'receita_id': 5, 'usuario_id': 20}
        result = dao.remover_do_cardapio(dados)

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('dao.cardapio_dao.sqlite3.connect')
    def test_visualizar_receitas_cardapio(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {'dia_semana': 'Segunda', 'tipo': 'Almoço', 'id_receita_FK': 1},
            {'dia_semana': 'Segunda', 'tipo': 'Almoço', 'id_receita_FK': 2},
            {'dia_semana': 'Terça', 'tipo': 'Jantar', 'id_receita_FK': 3}
        ]

        dao = CardapioDAO("fake_path.db")
        resultado = dao.visualizar_receitas_cardapio(usuario_id=1)

        self.assertEqual(resultado['Segunda']['Almoço'], ['1', '2'])
        self.assertEqual(resultado['Terça']['Jantar'], ['3'])
        self.assertEqual(resultado['Quarta']['Café da Manhã'], [])
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
