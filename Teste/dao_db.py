import sqlite3

class BancoDeDados:
    def __init__(self, nome_banco="sistema_receitas.db"):
        self.conn = sqlite3.connect(nome_banco)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT,
                senha TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Amizade (
                id INTEGER PRIMARY KEY,
                id_usuario1 INTEGER,
                id_usuario2 INTEGER,
                receita_id INTEGER,
                FOREIGN KEY (id_usuario1) REFERENCES Usuario(id),
                FOREIGN KEY (id_usuario2) REFERENCES Usuario(id),
                FOREIGN KEY (receita_id) REFERENCES Receita(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Receita (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                porcao INTEGER,
                tempo_preparo INTEGER,
                tipo TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario_receita (
                usuario_id INTEGER,
                receita_id INTEGER,
                PRIMARY KEY (usuario_id, receita_id),
                FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
                FOREIGN KEY (receita_id) REFERENCES Receita(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ingredientes (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                quantidade REAL,
                unidade TEXT,
                id_receita_FK INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Cardapio (
                id INTEGER PRIMARY KEY,
                refeicoes_Cardapio_FK INTEGER,
                id_usuario_FK INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Refeicoes_Cardapio (
                id INTEGER PRIMARY KEY,
                dia_semana TEXT,
                tipo TEXT,
                id_receita_FK INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Preparos (
                id INTEGER PRIMARY KEY,
                etapa INTEGER,
                descricao TEXT,
                id_receita_FK INTEGER,
                FOREIGN KEY (id_receita_FK) REFERENCES Receita(id)
            )
        """)
        self.conn.commit()

    def fechar(self):
        self.conn.close()

