import logica_db as db 
import os
import sys

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def executar_script(nome_script):
    interpretador = sys.executable 
    try:
        print(f"\nExecutando {nome_script}...")
        os.system(f"{interpretador} {nome_script}")
        print(f"\n {nome_script} executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar {nome_script}: {e}")

def consultar_views():
    while True:
        limpar_tela()
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
                    print(f"ID {id:<4} | {nome:<25} | R$ {total or 0:.2f}")
            else:
                print("Nenhum dado encontrado (execute 'popular_dados.py').")
        elif opcao == "2":
            resultados = db.get_view_total_vendido()
            print("\n TOTAL VENDIDO POR VENDEDOR")
            print("-" * 45)
            if resultados:
                for id, nome, total in resultados:
                    print(f"ID {id:<4} | {nome:<25} | R$ {total or 0:.2f}")
            else:
                print("Nenhum dado encontrado (execute 'popular_dados.py').")
        elif opcao == "3":
            resultados = db.get_view_produtos_mais_vendidos()
            print("\n PRODUTOS MAIS VENDIDOS")
            print("-" * 45)
            if resultados:
                for id, nome, qtd in resultados:
                    print(f"ID {id:<4} | {nome:<25} | Quantidade: {int(qtd or 0)}")
            else:
                print("Nenhum dado encontrado (execute 'popular_dados.py').")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        input("\nPressione Enter para continuar...")

def menu_cliente():
    while True:
        limpar_tela()
        print("\n === MENU CLIENTE ===")
        print("[1] Cadastrar Novo Cliente")
        print("[2] Testar Função 'Calcula_idade'")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            try:
                print("\n--- Cadastro de Novo Cliente ---")
                nome = input("Nome completo: ")
                sexo = input("Sexo (m/f/o): ").lower()
                data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
                
                if sexo not in ['m', 'f', 'o']:
                    print("Sexo inválido.")
                else:
                    db.cadastrar_cliente(nome, sexo, data_nasc)
                    
            except Exception as e:
                print(f"Erro nos dados: {e}")
                
        elif opcao == "2":
            try:
                id_cli = int(input("Digite o ID do cliente: "))
                idade = db.chamar_calcula_idade(id_cli)
                if idade is not None:
                    print(f"A idade calculada do Cliente {id_cli} é: {idade} anos.")
                else:
                    print(f"Cliente {id_cli} não encontrado.")
            except ValueError:
                print("ID inválido.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("\nPressione Enter para continuar...")

def menu_vendedor():
    while True:
        limpar_tela()
        print("\n === MENU VENDEDOR (Funcionário) ===")
        print("[1] Realizar Venda (Chama Procedure)")
        print("[2] Cadastrar Novo Produto")
        print("[0] Voltar")

        opcao = input("Escolha uma opção:")
        if opcao == "1":
            try:
                print("\n--- Registrar Nova Venda ---")
                id_cli = int(input("ID do Cliente: "))
                id_vend = int(input("ID do Vendedor (seu ID): "))
                id_trans = int(input("ID da Transportadora: "))
                end = input("Endereço de Entrega: ")
                id_prod = int(input("ID do Produto vendido: "))
                db.chamar_realizar_venda(id_cli, id_vend, id_trans, end, id_prod)
            except ValueError:
                print("IDs devem ser números.")
        elif opcao == "2":
            try:
                print("\n--- Cadastro de Novo Produto ---")
                nome = input("Nome do produto: ")
                estoque = int(input("Quantidade em estoque: "))
                valor = float(input("Valor (ex: 199.90): "))
                desc = input("Descrição: ")
                id_vend = int(input("ID do Vendedor (proprietário): "))
                db.cadastrar_produto(nome, estoque, valor, desc, id_vend)
            except ValueError:
                print("Valores numéricos inválidos.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("\nPressione Enter para continuar...")

def menu_gerente():
    while True:
        limpar_tela()
        print("\n=== MENU GERENTE ===")
        print("[1] Consultar Views (Relatórios)")
        print("[2] Ver Estatísticas (Procedure)")
        print("[3] Testar Função 'Soma_fretes'")
        print("[4] Testar Função 'Arrecadado'")
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
                    if not res_bloco:
                        print("(Sem dados)")
                    for linha in res_bloco:
                        print(linha)
            else:
                print("Nenhum dado encontrado.")
        elif opcao == "3":
            try:
                destino = input("Digite o destino (exato): ")
                total = db.chamar_soma_fretes(destino)
                print(f"Total de fretes para '{destino}': R$ {total:.2f}")
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "4":
            try:
                data = input("Data (AAAA-MM-DD): ")
                id_vend = int(input("ID do Vendedor: "))
                total = db.chamar_arrecadado(data, id_vend)
                print(f"Total arrecadado por Vendedor {id_vend} em {data}: R$ {total:.2f}")
            except ValueError:
                print("ID inválido.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
        input("\nPressione Enter para continuar...")

def menu_adm():
    while True:
        limpar_tela()
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
                print("Valor inválido.")
        elif opcao == "2":
            resultado = db.chamar_sorteio()
            if resultado:
                print("\n--- RESULTADO DO SORTEIO ---")
                print(f"Cliente Sorteado: {resultado[0]}")
                print(f"Valor do Voucher: R$ {resultado[1]:.2f}")
        elif opcao == "3":
            consultar_views()
        elif opcao == "0":
            break
        else:         
            print("Opção inválida")
        input("\nPressione Enter para continuar...")

def menu_setup():
    while True:
        limpar_tela()
        print("\n === MENU DE SETUP DO BANCO DE DADOS ===")
        print("ATENÇÃO: Use apenas se souber o que está a fazer.")
        print("\n[1] CRIAR a estrutura completa (criar_db.py)")
        print("[2] POPULAR o banco com dados (popular_dados.py)")
        print("[3] DESTRUIR o banco de dados (destruir_banco.py)")
        print("[0] Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("Isto irá criar todas as tabelas, funções, views, etc.")
            confirma = input("Tem a certeza? (s/n): ").lower()
            if confirma == 's':
                executar_script("criar_db.py")
            else:
                print("Operação cancelada.")
                
        elif opcao == "2":
            print("Isto irá inserir 100 clientes, 20 produtos e 150 vendas.")
            confirma = input("Tem a certeza? (s/n): ").lower()
            if confirma == 's':
                executar_script("popular_dados.py")
            else:
                print("Operação cancelada.")
                
        elif opcao == "3":
            print("!!! PERIGO !!! Isto irá apagar o banco 'ecommerce_oculos_db'!")
            confirma = input("Tem a MESMO a certeza? (s/n): ").lower()
            if confirma == 's':
                executar_script("destruir_banco.py")
            else:
                print("Operação cancelada.")
                
        elif opcao == "0":
            break
        else:
            print("Opção inválida")
            
        input("\nPressione Enter para continuar...")

def main():
    while True:
        limpar_tela()
        print("\n=== BEM-VINDO AO E-COMMERCE DE ÓCULOS ===")
        print("\n[1] Acessar o Sistema (Menus de Perfil)")
        print("[2] Setup do Banco de Dados (Admin)")
        print("[0] Sair da Aplicação")

        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_perfis()
        elif opcao == "2":
            menu_setup()
        elif opcao == "0":
            print("Encerrando aplicação. Até logo!")
            break
        else:
            print("Opção inválida")           

def menu_perfis():
    while True:
        limpar_tela()
        print("\n=== MENU PRINCIPAL (PERFIS) ===")
        print("[1] Gerência Clientes")
        print("[2] Sou Vendedor (Funcionário)")
        print("[3] Sou Gerente")
        print("[4] Sou Administrador")
        print("[0] Voltar ao Menu Inicial")

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
            break
        else:
            print("Opção inválida")
        
if __name__ == "__main__":
    main()