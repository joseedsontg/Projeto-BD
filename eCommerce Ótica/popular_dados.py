# 2_popular_banco.py (Revisão Final)
import mysql.connector
from mysql.connector import errorcode
from config import HOST, USUARIO, SENHA
from faker import Faker
import random

NOME_BANCO = "ecommerce_oculos_db"

# Inicializa o Faker para gerar dados em português
fake = Faker('pt_BR')

def inserir_dados():
    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=USUARIO,
            password=SENHA,
            database=NOME_BANCO
        )
        cursor = cnx.cursor()

        print("Conectado! Iniciando a inserção de dados (Esquema Final)...")

        # --- 1. Inserir Vendedores (5) ---
        vendedores = []
        for _ in range(5):
            vendedores.append((
                fake.name(),
                fake.sentence(nb_words=4), # Causa social
                random.uniform(3.5, 5.0), # Nota media
                random.uniform(1500.0, 5000.0), # Salário
            ))
            
        sql_vendedores = """
        INSERT INTO Vendedor (nome, causa_social, nota_media, salario)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(sql_vendedores, vendedores)
        print(f"{cursor.rowcount} vendedores inseridos.")

        # --- 2. Inserir Transportadoras (3) ---
        transportadoras = [
            ('RápidoLog', 'São Paulo'),
            ('VelozEntregas', 'Rio de Janeiro'),
            ('BrasilCargo', 'Curitiba')
        ]
        sql_transportadoras = "INSERT INTO Transportadora (nome, cidade) VALUES (%s, %s)"
        cursor.executemany(sql_transportadoras, transportadoras)
        print(f"{cursor.rowcount} transportadoras inseridas.")

        # --- 3. Inserir Clientes (100) ---
        clientes = []
        for _ in range(100):
            clientes.append((
                fake.name(),
                random.choice(['m', 'f', 'o']),
                fake.date_of_birth(minimum_age=18, maximum_age=80)
            ))
        sql_clientes = """
        INSERT INTO Cliente (nome, sexo, data_de_nascimento) VALUES (%s, %s, %s)
        """
        cursor.executemany(sql_clientes, clientes)
        print(f"{cursor.rowcount} clientes inseridos.")

        # --- 4. Inserir Produtos (20) ---
        produtos = []
        for _ in range(20):
            produtos.append((
                f"Óculos {fake.word().capitalize()} {random.choice(['Sport', 'Classic', 'Modern'])}",
                random.randint(10, 100), # Estoque
                round(random.uniform(99.90, 799.90), 2), # Valor
                fake.sentence(nb_words=10), # Descrição
                random.randint(1, 5) # id_vendedor (assume IDs 1-5)
            ))
        sql_produtos = """
        INSERT INTO Produto (nome, quantidade_em_estoque, valor, descricao, id_vendedor)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql_produtos, produtos)
        print(f"{cursor.rowcount} produtos inseridos.")

        cnx.commit()
        print("\n(Revisão Final) Todos os dados iniciais foram inseridos com sucesso!")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Verifique o nome de usuário ou senha no config.py")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Erro: Banco de dados '{NOME_BANCO}' não existe.")
            print("Execute o script '1_criar_banco.py' primeiro.")
        else:
            print(f"Erro ao inserir dados: {err}")
    finally:
        if cursor: cursor.close()
        if cnx: cnx.close()

if __name__ == "__main__":
    inserir_dados()