from dao_db import BancoDeDados # e outras classes que quiser usar
import sqlite3


class Usuario:
    def __init__(self, id, nome, email, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def salvar_receita(self, receita_id, banco: BancoDeDados):
        try:
            banco.cursor.execute("""
                INSERT INTO usuario_receita (usuario_id, receita_id)
                VALUES (?, ?)
            """, (self.id, receita_id))
            banco.conn.commit()
            print(f"Receita {receita_id} salva por {self.nome}.")
        except sqlite3.IntegrityError:
            print("Esta receita já foi salva por este usuário.")

    def listar_receitas(self, banco: BancoDeDados):
        banco.cursor.execute("""
            SELECT DISTINCT r.id, r.nome FROM Receita r
            JOIN usuario_receita ur ON r.id = ur.receita_id
            LEFT JOIN Amizade a ON r.id = a.receita_id
            WHERE ur.usuario_id = ? OR a.id_usuario2 = ?
        """, (self.id, self.id))
        receitas = banco.cursor.fetchall()
        print(f"Receitas associadas ao usuário {self.nome}:")
        for r in receitas:
            print(f"- {r[1]} (id={r[0]})")

    def compartilhar_receita(self, banco: BancoDeDados, amigo: 'Usuario', receita_id: int):
        banco.cursor.execute("""
            INSERT INTO Amizade (id_usuario1, id_usuario2, receita_id)
            VALUES (?, ?, ?)
        """, (self.id, amigo.id, receita_id))
        banco.conn.commit()
        print(f"{self.nome} compartilhou a receita {receita_id} com {amigo.nome}.")

    def visualizar_receitas_compartilhadas_comigo(self, banco: BancoDeDados):
        banco.cursor.execute("""
            SELECT r.id, r.nome, u.nome FROM Receita r
            JOIN Amizade a ON r.id = a.receita_id
            JOIN Usuario u ON a.id_usuario1 = u.id
            WHERE a.id_usuario2 = ?
        """, (self.id,))
        compartilhadas = banco.cursor.fetchall()
        print(f"Receitas compartilhadas com {self.nome}:")
        for r in compartilhadas:
            print(f"- {r[1]} (id={r[0]}) compartilhada por {r[2]}")


class Amizade:
    def __init__(self, id, id_usuario1, id_usuario2, receita_id):
        self.id = id
        self.id_usuario1 = id_usuario1
        self.id_usuario2 = id_usuario2
        self.receita_id = receita_id

class Receita:
    def __init__(self, id, nome, porcao, tempo_preparo, tipo):
        self.id = id
        self.nome = nome
        self.porcao = porcao
        self.tempo_preparo = tempo_preparo
        self.tipo = tipo
       
    def salvar_no_banco(self, banco: BancoDeDados):
        banco.cursor.execute("""
            INSERT INTO Receita (nome, porcao, tempo_preparo, tipo)
            VALUES (?, ?, ?, ?)
        """, (self.nome, self.porcao, self.tempo_preparo, self.tipo))
        banco.conn.commit()
        self.id = banco.cursor.lastrowid
        print(f"Receita '{self.nome}' salva com sucesso no banco.")
    def listar_etapas_preparo(self, banco: BancoDeDados):
        banco.cursor.execute("""
            SELECT etapa, descricao FROM Preparos
            WHERE id_receita_FK = ?
            ORDER BY etapa
        """, (self.id,))
        etapas = banco.cursor.fetchall()
        print(f"Modo de preparo para {self.nome}:")
        for etapa in etapas:
            print(f"Etapa {etapa[0]}: {etapa[1]}")

class Preparos:
    def __init__(self, id, etapa, descricao, id_receita_FK):
        self.id = id
        self.etapa = etapa
        self.descricao = descricao
        self.id_receita_FK = id_receita_FK

    def salvar_no_banco(self, banco: BancoDeDados):
        banco.cursor.execute("""
            INSERT INTO Preparos (etapa, descricao, id_receita_FK)
            VALUES (?, ?, ?)
        """, (self.etapa, self.descricao, self.id_receita_FK))
        banco.conn.commit()
        print(f"Etapa {self.etapa} da receita {self.id_receita_FK} salva.")

class Ingredientes:
    def __init__(self, id, nome, quantidade, unidade):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.unidade = unidade


class Cardapio:
    def __init__(self, id, refeicoes_Cardapio):
        self.id = id
        self.refeicoes_Cardapio = refeicoes_Cardapio


class Refeicoes_Cardapio:
    def __init__(self, id, dia_semana, tipo):
        self.id = id
        self.dia_semana = dia_semana
        self.tipo = tipo


if __name__ == "__main__":
    banco = BancoDeDados()

    # Limpeza das tabelas para garantir teste limpo
    banco.cursor.execute("DELETE FROM Usuario")
    banco.cursor.execute("DELETE FROM Receita")
    banco.cursor.execute("DELETE FROM Amizade")
    banco.cursor.execute("DELETE FROM usuario_receita")
    banco.cursor.execute("DELETE FROM Preparos")
    banco.conn.commit()

    # Criar usuários
    banco.cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)", ("Maria", "maria@email.com", "123"))
    banco.cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)", ("João", "joao@email.com", "456"))
    banco.conn.commit()

    banco.cursor.execute("SELECT * FROM Usuario WHERE email = 'maria@email.com'")
    dados_maria = banco.cursor.fetchone()
    banco.cursor.execute("SELECT * FROM Usuario WHERE email = 'joao@email.com'")
    dados_joao = banco.cursor.fetchone()

    maria = Usuario(*dados_maria)
    joao = Usuario(*dados_joao)

    # Criar e salvar receita
    banco.cursor.execute("""
        INSERT INTO Receita (nome, porcao, tempo_preparo, tipo) 
        VALUES (?, ?, ?, ?)
    """, ("Bolo de Morango", 10, 60, "Doce"))
    banco.conn.commit()

    receita_id = banco.cursor.lastrowid
    receita_bolo = Receita(receita_id, "Bolo de Morango", 10, 60, "Doce")

    # Etapas de preparo
    etapas = [
        ("Pré-aqueça o forno a 180°C.", 1),
        ("Misture os ingredientes secos.", 2),
        ("Adicione os líquidos e bata.", 3)
    ]

    for idx, (desc, etapa_num) in enumerate(etapas, start=1):
        banco.cursor.execute("""
            INSERT INTO Preparos (id, etapa, descricao, id_receita_FK)
            VALUES (?, ?, ?, ?)
        """, (idx, etapa_num, desc, receita_bolo.id))
    banco.conn.commit()

    # Maria salva e compartilha a receita com João
    maria.salvar_receita(receita_bolo.id, banco)
    maria.compartilhar_receita(banco, joao, receita_bolo.id)

    print("\n--- Receitas de Maria ---")
    maria.listar_receitas(banco)

    print("\n--- Receitas de João ---")
    joao.listar_receitas(banco)

    print("\n--- Receitas compartilhadas com João ---")
    joao.visualizar_receitas_compartilhadas_comigo(banco)

    print("\n--- Etapas de preparo da receita ---")
    banco.cursor.execute("""
        SELECT etapa, descricao FROM Preparos 
        WHERE id_receita_FK = ? ORDER BY etapa
    """, (receita_bolo.id,))
    etapas_result = banco.cursor.fetchall()
    for etapa, desc in etapas_result:
        print(f"Etapa {etapa}: {desc}")

print("testado")
    



