from database import criar_tabelas
from estoque import (
    cadastrar_produto, listar_produtos, buscar_produto,
    atualizar_produto, excluir_produto, movimentar_estoque,
    gerar_relatorio, listar_movimentacoes
)


def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um número igual ou maior que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_preco(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor < 0:
                print("O preço não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("Preço inválido. Exemplo: 19.90")


def exibir_produtos(produtos):
    if not produtos:
        print("\nNenhum produto encontrado.")
        return

    print("\n" + "-" * 78)
    print(f"{'ID':<5}{'NOME':<25}{'CATEGORIA':<18}{'PREÇO (R$)':>13}{'QTD.':>10}")
    print("-" * 78)
    for produto in produtos:
        produto_id, nome, categoria, preco, quantidade = produto
        print(f"{produto_id:<5}{nome[:23]:<25}{categoria[:16]:<18}"
              f"{preco:>13.2f}{quantidade:>10}")
    print("-" * 78)


def menu():
    print("""
========== SISTEMA DE GERENCIAMENTO DE ESTOQUE ==========
1 - Cadastrar produto
2 - Listar produtos
3 - Buscar produto
4 - Atualizar produto
5 - Excluir produto
6 - Registrar entrada no estoque
7 - Registrar saída do estoque
8 - Relatório do estoque
9 - Histórico de movimentações
0 - Sair
=========================================================
""")


def executar():
    criar_tabelas()
    print("Bem-vindo ao Sistema de Gerenciamento de Estoque!")

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do produto: ").strip()
            categoria = input("Categoria: ").strip()
            if not nome or not categoria:
                print("Nome e categoria são obrigatórios.")
                continue
            preco = ler_preco("Preço (R$): ")
            quantidade = ler_inteiro("Quantidade inicial: ", 0)
            produto_id = cadastrar_produto(nome, categoria, preco, quantidade)
            print(f"Produto cadastrado com sucesso! ID: {produto_id}")

        elif opcao == "2":
            exibir_produtos(listar_produtos())

        elif opcao == "3":
            termo = input("Digite o ID ou parte do nome: ").strip()
            exibir_produtos(buscar_produto(termo))

        elif opcao == "4":
            produto_id = ler_inteiro("ID do produto: ", 1)
            produto = buscar_produto(str(produto_id))
            if not produto:
                print("Produto não encontrado.")
                continue
            nome = input(f"Novo nome [{produto[0][1]}]: ").strip() or produto[0][1]
            categoria = input(
                f"Nova categoria [{produto[0][2]}]: ").strip() or produto[0][2]
            preco_digitado = input(
                f"Novo preço [{produto[0][3]:.2f}]: ").strip()
            preco = (ler_preco("Novo preço: ") if preco_digitado == ""
                     else float(preco_digitado.replace(",", ".")))
            if preco < 0:
                print("O preço não pode ser negativo.")
                continue
            if atualizar_produto(produto_id, nome, categoria, preco):
                print("Produto atualizado com sucesso.")

        elif opcao == "5":
            produto_id = ler_inteiro("ID do produto que deseja excluir: ", 1)
            confirmar = input("Tem certeza? (s/n): ").strip().lower()
            if confirmar == "s":
                sucesso, mensagem = excluir_produto(produto_id)
                print(mensagem)

        elif opcao in ("6", "7"):
            produto_id = ler_inteiro("ID do produto: ", 1)
            quantidade = ler_inteiro("Quantidade: ", 1)
            tipo = "ENTRADA" if opcao == "6" else "SAIDA"
            sucesso, mensagem = movimentar_estoque(produto_id, tipo, quantidade)
            print(mensagem)

        elif opcao == "8":
            total_produtos, total_unidades, valor_total = gerar_relatorio()
            print("\n========== RELATÓRIO DO ESTOQUE ==========")
            print(f"Tipos de produtos cadastrados: {total_produtos}")
            print(f"Unidades disponíveis: {total_unidades}")
            print(f"Valor total estimado: R$ {valor_total:.2f}")
            print("==========================================")

        elif opcao == "9":
            movimentacoes = listar_movimentacoes()
            if not movimentacoes:
                print("Nenhuma movimentação registrada.")
            else:
                print("\nID | PRODUTO | TIPO | QUANTIDADE | DATA/HORA")
                for mov in movimentacoes:
                    print(f"{mov[0]} | {mov[1]} | {mov[2]} | {mov[3]} | {mov[4]}")

        elif opcao == "0":
            print("Sistema encerrado. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    executar()
