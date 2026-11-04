import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "estoque.db"


def conectar():
    """Abre uma conexão com o banco de dados SQLite."""
    return sqlite3.connect(DB_PATH)


def criar_tabelas():
    """Cria as tabelas necessárias caso elas ainda não existam."""
    with conectar() as conexao:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL CHECK(preco >= 0),
                quantidade INTEGER NOT NULL CHECK(quantidade >= 0)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('ENTRADA', 'SAIDA')),
                quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)
        conexao.commit()
