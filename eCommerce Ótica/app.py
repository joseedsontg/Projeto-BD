from conectar import ligar
from criar_db import Cliente, Vendedor
import mysql.connector
from config import HOST, USUARIO, SENHA

# -------------------------------------
# Funções auxiliares de conexão e views
# -------------------------------------
def conectar():
    """Conecta ao banco de dados principal."""
    try:
        con = mysql.connector.connect(
            host=HOST,
            user=USUARIO,
            password=SENHA,
            database="ecommerce_oculos_db"
        )
        return con
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco: {err}")
        return None

def exibir_total_gasto_por_cliente(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_total_gasto_por_cliente")
    resultados = cursor.fetchall()
    print("\n💰 TOTAL GASTO POR CLIENTE")
    print("-" * 45)
    for nome, total in resultados:
        print(f"{nome:<25} | R$ {total:.2f}")
    cursor.close()

def exibir_total_vendido_por_vendedor(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_total_vendido_por_vendedor")
    resultados = cursor.fetchall()
    print("\n🧾 TOTAL VENDIDO POR VENDEDOR")
    print("-" * 45)
    for nome, total in resultados:
        print(f"{nome:<25} | R$ {total:.2f}")
    cursor.close()

def exibir_produtos_mais_vendidos(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_produtos_mais_vendidos")
    resultados = cursor.fetchall()
    print("\n📦 PRODUTOS MAIS VENDIDOS")
    print("-" * 45)
    for nome, qtd in resultados:
        print(f"{nome:<25} | Quantidade vendida: {int(qtd)}")
    cursor.close()

def consultar_views():
    """Submenu para exibir as views."""
    con = conectar()
    if not con:
        print("❌ Erro ao conectar no banco de dados.")
        return

    while True:
        print("\n=== CONSULTAS (VIEWS) ===")
        print("[1] Total gasto por cliente")
        print("[2] Total vendido por vendedor")
        print("[3] Produtos mais vendidos")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_total_gasto_por_cliente(con)
        elif opcao == "2":
            exibir_total_vendido_por_vendedor(con)
        elif opcao == "3":
            exibir_produtos_mais_vendidos(con)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
    con.close()

# -------------------------------------
# Menus de usuário
# -------------------------------------
def menu_cliente(id_cliente=None):
    usuario = Cliente(id_cliente)
    while True:
        print("\n === MENU CLIENTE ===")
        print("[1] Cadastrar")
        print("[2] Login")
        print("[3] Compras")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Cadastro em andamento...")
        elif opcao == "2":
            print("Login em andamento...")
        elif opcao == "3":
            print("Abrindo área de compras...")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_vendedor(id_vendedor=None):
    vendedor = Vendedor(id_vendedor)
    while True:
        print("\n === MENU VENDEDOR ===")
        print("[1] Login")
        print("[2] Consulta")
        print("[3] Adicionar produto")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Login de vendedor...")
        elif opcao == "2":
            print("Consultando dados...")
        elif opcao == "3":
            print("Adicionando produto...")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_gerente(id_vendedor=None):
    gerente = Vendedor(id_vendedor)
    while True:
        print("\n=== MENU GERENTE ===")
        print("[1] Buscar")
        print("[2] Apagar")
        print("[3] Editar")
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Busca em andamento...")
        elif opcao == "2":
            print("Apagando dados...")
        elif opcao == "3":
            print("Editando informações...")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_adm(id_vendedor=None):
    adm = Vendedor(id_vendedor)
    while True:
        print("\n === MENU ADMINISTRADOR ===")
        print("[1] Buscar")
        print("[2] Apagar")
        print("[3] Editar")             
        print("[4] Adicionar")             
        print("[5] Consultar (simples)")  
        print("[6] Consultar Views (Relatórios)")  
        print("[0] Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            print("Buscando registros...")
        elif opcao == "2":
            print("Apagando registros...")
        elif opcao == "3":
            print("Editando registros...")
        elif opcao == "4":
            print("Adicionando registros...")
        elif opcao == "5":
            print("Consultando informações...")
        elif opcao == "6":
            consultar_views()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

# -------------------------------------
# Menu principal
# -------------------------------------
def main():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("[1] Cliente")
        print("[2] Vendedor")
        print("[3] Gerente")
        print("[4] Administrador")
        print("[0] Sair")

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
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
