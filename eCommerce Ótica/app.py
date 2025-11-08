from conectar import ligar
from criar_db import Cliente # Assumindo que Cliente é o "Usuário"
from criar_db import Vendedor
# Assumindo que você tem uma classe Administrador
# from criar_db import Administrador # <--- Descomente se Administrador estiver em criar_db
class Administrador: # Exemplo simples se você não a importou
    def __init__(self, id_admin):
        self.id_admin = id_admin
    def login(self):
        print(f"Admin ID {self.id_admin} logado.")
    def listar_tudo(self):
        print("Listando todos os dados do sistema...")
    def apagar_registro(self):
        print("Apagando registro no sistema...")


def menu_cliente(id_cliente=None): # Renomeei para menu_cliente para consistência
    # O id_cliente pode ser None se a opção for 'Cadastrar'
    
    while True:
        print("\n=== MENU CLIENTE/USUÁRIO ===")
        print("[1] Login")
        print("[2] Cadastrar Novo Cliente")
        print("[3] Apagar Conta")
        print("[0] Voltar ao Menu Geral")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_cliente = int(input("Digite seu ID para Login: "))
                usuario = Cliente(id_cliente)
                usuario.login() # Chamada de método da classe Cliente
                # Aqui você chamaria o menu de funcionalidades internas do cliente
                print("✅ Login de Cliente realizado. Menu de funcionalidades em desenvolvimento...")
            except ValueError:
                print("❌ ID inválido. Digite um número.")
        
        elif opcao == "2":
            print("➡️  Iniciando cadastro de Cliente...")
            # Lógica de cadastro (ex: pedir nome, email, senha)
            # Cliente.cadastrar_novo(...)
            print("✅ Cliente cadastrado com sucesso! Volte para fazer login.")

        elif opcao == "3":
            if id_cliente is not None:
                confirmar = input(f"Tem certeza que deseja apagar a conta ID {id_cliente}? (s/n): ")
                if confirmar.lower() == 's':
                    usuario = Cliente(id_cliente)
                    usuario.apagar() # Chamada de método da classe Cliente
                    print("🗑️  Conta apagada. Voltando ao Menu Geral.")
                    break
            else:
                print("⚠️ Você precisa fazer Login primeiro para apagar sua conta.")

        elif opcao == "0":
            print("⬅️  Voltando ao Menu Geral...")
            break
        
        else:
            print("⚠️ Opção inválida.")


def menu_vendedor(id_vendedor=None):
    
    while True:
        print("\n=== MENU VENDEDOR ===")
        print("[1] Login")
        print("[2] Cadastrar Novo Vendedor")
        print("[0] Voltar ao Menu Geral")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_vendedor = int(input("Digite seu ID para Login: "))
                vendedor = Vendedor(id_vendedor)
                vendedor.login() # Chamada de método da classe Vendedor
                # Aqui você chamaria o menu de funcionalidades internas do vendedor
                print("✅ Login de Vendedor realizado. Menu de funcionalidades em desenvolvimento...")
            except ValueError:
                print("❌ ID inválido. Digite um número.")

        elif opcao == "2":
            print("➡️  Iniciando cadastro de Vendedor...")
            # Lógica de cadastro (ex: pedir nome, CNPJ, etc.)
            # Vendedor.cadastrar_novo(...)
            print("✅ Vendedor cadastrado com sucesso! Volte para fazer login.")
        
        elif opcao == "0":
            print("⬅️  Voltando ao Menu Geral...")
            break

        else:
            print("⚠️ Opção inválida.")


def menu_administrador(id_administrador=None):
    
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("[1] Login (Acesso Restrito)")
        print("[0] Voltar ao Menu Geral")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                id_admin = int(input("Digite seu ID de Administrador: "))
                senha = input("Digite a senha: ") # Adicionando um campo de senha
                
                # Simular validação de login (usando o ID)
                if id_admin == 999 and senha == "admin123": # Exemplo de credenciais fixas
                    administrador = Administrador(id_admin)
                    administrador.login()
                    print("✅ Login de Administrador realizado. Acesso total.")
                    administrador.listar_tudo()
                    # Aqui você chamaria o menu de funcionalidades internas do administrador
                    # Ex: menu_funcionalidades_admin(administrador)
                else:
                    print("❌ ID ou Senha do Administrador inválidos.")
            except ValueError:
                print("❌ ID inválido. Digite um número.")

        elif opcao == "0":
            print("⬅️  Voltando ao Menu Geral...")
            break
        
        else:
            print("⚠️ Opção inválida.")


## 🌟 MENU GERAL INTEGRADO

def main():
    print("\n\n*** BEM-VINDO AO SISTEMA ***")
    
    while True:
        print("\n===========================")
        print("     MENU GERAL DE ACESSO")
        print("===========================")
        print("[1] Acesso Cliente/Usuário")
        print("[2] Acesso Vendedor")
        print("[3] Acesso Administrador")
        print("[0] Sair do Sistema")
        print("---------------------------")
        
        opcao = input("Escolha o tipo de acesso (0-3): ").strip()

        if opcao == "1":
            menu_cliente()
        elif opcao == "2":
            menu_vendedor()
        elif opcao == "3":
            menu_administrador()
        elif opcao == "0":
            print("\n👋 Sistema encerrado. Obrigado!")
            break
        else:
            print("⚠️ Opção inválida. Por favor, escolha 1, 2, 3 ou 0.")


if __name__ == "__main__":
    main()