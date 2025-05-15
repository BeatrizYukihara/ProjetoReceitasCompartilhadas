import unittest
import sqlite3
from dao.receita_dao import ReceitaDAO
from models.receita import Receita, Preparos, Ingrediente

class TestReceitaDAO(unittest.TestCase):
    def setUp(self):
        # Usar banco em memória para testes
        self.db_path = ':memory:'
        self.dao = ReceitaDAO(self.db_path)

        # Criar conexão direta só para criar as tabelas necessárias
        self.conn = sqlite3.connect(self.db_path)
        self.criar_tabelas()
        self.conn.close()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
            CREATE TABLE Receita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                porcao INTEGER,
                tempo_preparo INTEGER,
                tipo TEXT,
                preco REAL
            );
            CREATE TABLE Ingredientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                quantidade REAL,
                unidade TEXT,
                id_receita_FK INTEGER
            );
            CREATE TABLE Preparos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                etapa INTEGER,
                descricao TEXT,
                id_receita_FK INTEGER
            );
            CREATE TABLE usuario_receita (
                usuario_id INTEGER,
                receita_id INTEGER
            );
        """)
        self.conn.commit()

    def test_inserir_listar_receita(self):
        receita = Receita(None, 'Pizza', 4, 30, 'Salgada', 40.0)
        ingredientes = [
            Ingrediente(None, 'Farinha', 500, 'g', None),
            Ingrediente(None, 'Molho', 200, 'ml', None)
        ]
        preparos = [
            Preparos(None, 1, 'Misturar ingredientes', None),
            Preparos(None, 2, 'Assar por 20 minutos', None)
        ]

        self.dao.inserir(receita, ingredientes, preparos, usuario_id=123)

        resultados = self.dao.listar_por_usuario(123)
        self.assertEqual(len(resultados), 1)

        resultado = resultados[0]
        self.assertEqual(resultado['receita'].nome, 'Pizza')
        self.assertEqual(len(resultado['ingredientes']), 2)
        self.assertEqual(len(resultado['preparos']), 2)

    def test_excluir_receita(self):
        # Inserir para depois excluir
        receita = Receita(None, 'Sopa', 2, 20, 'Quente', 15.0)
        ingredientes = []
        preparos = []

        self.dao.inserir(receita, ingredientes, preparos, usuario_id=1)
        resultados = self.dao.listar_por_usuario(1)
        receita_id = resultados[0]['receita'].id

        self.dao.excluir(receita_id)

        resultados_apos_exclusao = self.dao.listar_por_usuario(1)
        self.assertEqual(len(resultados_apos_exclusao), 0)

    def test_atualizar_preco(self):
        receita = Receita(None, 'Bolo', 6, 50, 'Doce', 30.0)
        ingredientes = []
        preparos = []

        self.dao.inserir(receita, ingredientes, preparos, usuario_id=2)
        resultados = self.dao.listar_por_usuario(2)
        receita_id = resultados[0]['receita'].id

        self.dao.atualizar_preco(45.5, receita_id)

        resultados_atualizados = self.dao.listar_por_usuario(2)
        preco_atualizado = resultados_atualizados[0]['receita'].preco
        self.assertEqual(preco_atualizado, 45.5)

if __name__ == '__main__':
    unittest.main()
