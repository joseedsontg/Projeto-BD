# app.py
# (Corrigido para usar db_logic.py e o padrão procedural)

# Não importamos mais de 'criar_db'
import logica_db as db  # Importa o nosso novo ficheiro de lógica

# --- Submenus para Lógica ---

def consultar_views():
    """Submenu para exibir as views."""
    while True:
        print("\n=== CONSULTAS (VIEWS) ===")
        print("[1] Total gasto por cliente")
        print("[2] Total vendido por vendedor")
        print("[3] Produtos mais vendidos")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            resultados = db.get_view_total_gasto()
            print("\n TOTAL GASTO POR CLIENTE")
            print("-" * 45)
            if resultados:
                for id, nome, total in resultados:
                    print(f"ID {id} | {nome:<25} | R$ {total or 0:.2f}")
        elif opcao == "2":
            resultados = db.get_view_total_vendido()
            print("\n TOTAL VENDIDO POR VENDEDOR")
            print("-" * 45)
            if resultados:
                for id, nome, total in resultados:
                    print(f"ID {id} | {nome:<25} | R$ {total or 0:.2f}")
        elif opcao == "3":
            resultados = db.get_view_produtos_mais_vendidos()
            print("\n PRODUTOS MAIS VENDIDOS")
            print("-" * 45)
            if resultados:
                for id, nome, qtd in resultados:
                    print(f"ID {id} | {nome:<25} | Quantidade: {int(qtd or 0)}")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        input("Pressione Enter para continuar...")

def menu_cliente():
    while True:
        print("\n === MENU CLIENTE ===")
        print("[1] Cadastrar (Em breve)")
        print("[2] Login (Em breve)")
        print("[3] Testar Função 'Calcula_idade'")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Lógica de cadastro de cliente em breve...")
        elif opcao == "2":
            print("Lógica de login de cliente em breve...")
        elif opcao == "3":
            try:
                id_cli = int(input("Digite o ID do cliente: "))
                idade = db.chamar_calcula_idade(id_cli)
                if idade is not None:
                    print(f"✅ A idade calculada do Cliente {id_cli} é: {idade} anos.")
                else:
                    print(f"⚠  Cliente {id_cli} não encontrado.")
            except ValueError:
                print("❌ ID inválido.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("Pressione Enter para continuar...")

def menu_vendedor():
    while True:
        print("\n === MENU VENDEDOR (Funcionário) ===")
        print("[1] Realizar Venda (Chama Procedure)")
        print("[0] Voltar")

        opcao = input("Escolha uma opção:")
        if opcao == "1":
            try:
                id_cli = int(input("ID do Cliente: "))
                id_vend = int(input("ID do Vendedor (seu ID): "))
                id_trans = int(input("ID da Transportadora: "))
                end = input("Endereço de Entrega: ")
                id_prod = int(input("ID do Produto vendido: "))
                db.chamar_realizar_venda(id_cli, id_vend, id_trans, end, id_prod)
            except ValueError:
                print("❌ IDs devem ser números.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("Pressione Enter para continuar...")

def menu_gerente():
    while True:
        print("\n=== MENU GERENTE ===")
        print("[1] Consultar Views (Relatórios)")
        print("[2] Ver Estatísticas (Chama Procedure)")
        print("[0] Voltar")

        opcao = input("Escolha uma opção:")
        if opcao == "1":
            consultar_views()
        elif opcao == "2":
            resultados = db.chamar_estatisticas()
            if resultados:
                print("\n--- ESTATÍSTICAS COMPLETAS ---")
                for i, res_bloco in enumerate(resultados):
                    print(f"\nBloco de Estatística {i+1}:")
                    for linha in res_bloco:
                        print(linha)
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("Pressione Enter para continuar...")

def menu_adm():
    while True:
        print("\n === MENU ADMINISTRADOR ===")
        print("[1] Aplicar Reajuste Salarial (Procedure)")
        print("[2] Realizar Sorteio de Voucher (Procedure)")
        print("[3] Consultar Views (Relatórios)")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            try:
                perc = float(input("Digite o percentual de reajuste (ex: 10 para 10%): "))
                db.chamar_reajuste(perc)
            except ValueError:
                print("❌ Valor inválido.")
        elif opcao == "2":
            resultado = db.chamar_sorteio()
            if resultado:
                print("\n--- 🍀 RESULTADO DO SORTEIO 🍀 ---")
                print(f"Cliente Sorteado: {resultado[0]}")
                print(f"Valor do Voucher: R$ {resultado[1]:.2f}")
        elif opcao == "3":
            consultar_views()
        elif opcao == "0":
            break
        else:         
            print("Opção inválida")
        input("Pressione Enter para continuar...")

def main():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Sou Cliente")
        print("[2] Sou Vendedor (Funcionário)")
        print("[3] Sou Gerente")
        print("[4] Sou Administrador")
        print("[0] Sair da Aplicação")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            menu_cliente()
        elif opcao == "2":           
            menu_vendedor()
        elif opcao == "3":           
            menu_gerente()
        elif opcao == "4":           
            menu_adm()
        elif opcao == "0":
            print("👋 Encerrando aplicação. Até logo!")
            break
        else:
            print("Opção inválida")           
        
if __name__ == "__main__":
    main()