from database import conectar


def cadastrar_produto(nome, categoria, preco, quantidade):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, categoria, preco, quantidade)
            VALUES (?, ?, ?, ?)
        """, (nome, categoria, preco, quantidade))
        conexao.commit()
        return cursor.lastrowid


def listar_produtos():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id, nome, categoria, preco, quantidade
            FROM produtos
            ORDER BY nome
        """)
        return cursor.fetchall()


def buscar_produto(termo):
    with conectar() as conexao:
        cursor = conexao.cursor()
        if str(termo).isdigit():
            cursor.execute("""
                SELECT id, nome, categoria, preco, quantidade
                FROM produtos WHERE id = ?
            """, (int(termo),))
        else:
            cursor.execute("""
                SELECT id, nome, categoria, preco, quantidade
                FROM produtos WHERE nome LIKE ?
                ORDER BY nome
            """, (f"%{termo}%",))
        return cursor.fetchall()


def atualizar_produto(produto_id, nome, categoria, preco):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE produtos
            SET nome = ?, categoria = ?, preco = ?
            WHERE id = ?
        """, (nome, categoria, preco, produto_id))
        conexao.commit()
        return cursor.rowcount > 0


def excluir_produto(produto_id):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM movimentacoes WHERE produto_id = ?",
                       (produto_id,))
        possui_historico = cursor.fetchone()[0] > 0

        if possui_historico:
            return False, "Não é possível excluir: o produto possui movimentações."

        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conexao.commit()
        if cursor.rowcount == 0:
            return False, "Produto não encontrado."
        return True, "Produto excluído com sucesso."


def movimentar_estoque(produto_id, tipo, quantidade):
    if tipo not in ("ENTRADA", "SAIDA"):
        return False, "Tipo de movimentação inválido."

    if quantidade <= 0:
        return False, "A quantidade deve ser maior que zero."

    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        resultado = cursor.fetchone()

        if resultado is None:
            return False, "Produto não encontrado."

        estoque_atual = resultado[0]

        if tipo == "SAIDA" and quantidade > estoque_atual:
            return False, "Estoque insuficiente para essa saída."

        if tipo == "ENTRADA":
            nova_quantidade = estoque_atual + quantidade
        else:
            nova_quantidade = estoque_atual - quantidade

        cursor.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (nova_quantidade, produto_id)
        )
        cursor.execute("""
            INSERT INTO movimentacoes (produto_id, tipo, quantidade)
            VALUES (?, ?, ?)
        """, (produto_id, tipo, quantidade))
        conexao.commit()

    return True, f"{tipo.title()} registrada. Estoque atual: {nova_quantidade}."


def gerar_relatorio():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantidade), 0),
                COALESCE(SUM(preco * quantidade), 0)
            FROM produtos
        """)
        return cursor.fetchone()


def listar_movimentacoes():
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT m.id, p.nome, m.tipo, m.quantidade, m.data_hora
            FROM movimentacoes m
            INNER JOIN produtos p ON p.id = m.produto_id
            ORDER BY m.id DESC
        """)
        return cursor.fetchall()
