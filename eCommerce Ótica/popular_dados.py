import mysql.connector
from mysql.connector import errorcode
from config import HOST, USUARIO, SENHA
from faker import Faker
import random
from datetime import date

NOME_BANCO = "ecommerce_oculos_db"

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

        print("Conectado! Iniciando a inserção de dados...")

        cargos = [
            ('vendedor',), ('gerente',), ('CEO',)
        ]
        sql_cargos = "INSERT IGNORE INTO Cargo (nome) VALUES (%s)"
        cursor.executemany(sql_cargos, cargos)
        
        mapa_cargos = {}
        cursor.execute("SELECT id, nome FROM Cargo")
        for (id_cargo, nome_cargo) in cursor:
            mapa_cargos[nome_cargo] = id_cargo
            
        print(f"Cargos verificados/inseridos. Mapa de cargos: {mapa_cargos}")
        

        vendedores = []

        vendedores.append((
            fake.name(), 'Causa Social A', 'Óculos de Sol',
            random.uniform(3.5, 5.0), 2500.0, mapa_cargos['vendedor']
        ))
        vendedores.append((
            fake.name(), 'Causa Social B', 'Armações',
            random.uniform(3.5, 5.0), 2200.0, mapa_cargos['vendedor']
        ))
        vendedores.append((
            fake.name(), 'Causa Social C', 'Lentes',
            random.uniform(3.5, 5.0), 2300.0, mapa_cargos['vendedor']
        ))
        # 1 Gerente
        vendedores.append((
            fake.name(), 'Gestão de Equipa', 'Gerência',
            random.uniform(4.0, 5.0), 5500.0, mapa_cargos['gerente']
        ))
        # 1 Estagiário
        vendedores.append((
            fake.name(), 'Apoio Logístico', 'Logística',
            random.uniform(3.0, 4.0), 1200.0, mapa_cargos['CEO']
        ))

        sql_vendedores = """
        INSERT INTO Vendedor (nome, causa_social, tipo, nota_media, salario, id_cargo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(sql_vendedores, vendedores)
        print(f"{cursor.rowcount} vendedores inseridos.")

        transportadoras = [
            ('RápidoLog', 'São Paulo'),
            ('VelozEntregas', 'Rio de Janeiro'),
            ('BrasilCargo', 'Curitiba')
        ]
        sql_transportadoras = "INSERT INTO Transportadora (nome, cidade) VALUES (%s, %s)"
        cursor.executemany(sql_transportadoras, transportadoras)
        print(f"{cursor.rowcount} transportadoras inseridas.")

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

        produtos = []
        for _ in range(20):
            produtos.append((
                f"Óculos {fake.word().capitalize()} {random.choice(['Sport', 'Classic', 'Modern'])}",
                random.randint(10, 100),
                round(random.uniform(99.90, 799.90), 2),
                fake.sentence(nb_words=10),
                random.randint(1, 5)
            ))
        sql_produtos = """
        INSERT INTO Produto (nome, quantidade_em_estoque, valor, descricao, id_vendedor)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql_produtos, produtos)
        print(f"{cursor.rowcount} produtos inseridos.")

        cnx.commit()
        print("\nTodos os dados iniciais foram inseridos com sucesso!")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Verifique o nome de usuário ou senha no config.py")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Erro: Banco de dados '{NOME_BANCO}' não existe.")
            print("Execute o script '1_criar_banco.py' primeiro.")
        else:
            print(f"Erro ao inserir dados: {err}")
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

if __name__ == "__main__":
    inserir_dados()