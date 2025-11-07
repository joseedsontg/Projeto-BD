import mysql.connector
from mysql.connector import errorcode
from config import HOST, USUARIO, SENHA

NOME_BANCO = "ecommerce_oculos_db"

SQL_CREATE_DB = f"""
CREATE DATABASE IF NOT EXISTS {NOME_BANCO} 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

SCHEMA_SQL_TABELAS = [
"""
CREATE TABLE IF NOT EXISTS Cargo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(20) NOT NULL UNIQUE,

  CONSTRAINT chk_cargo_nome CHECK (nome IN ('vendedor', 'gerente', 'CEO'))
);
""",
"""
CREATE TABLE IF NOT EXISTS Cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  sexo VARCHAR(1),
  data_de_nascimento DATE NOT NULL,

  CONSTRAINT chk_sexo CHECK (sexo IN ('m', 'f', 'o'))
);
""",
"""
CREATE TABLE IF NOT EXISTS Vendedor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  causa_social VARCHAR(200) NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  nota_media FLOAT,
  salario FLOAT NOT NULL DEFAULT 0,
  id_cargo INT,
  FOREIGN KEY (id_cargo) REFERENCES Cargo(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Funcionario_Especial (
  id_vendedor INT PRIMARY KEY,
  bonus_total_acumulado FLOAT DEFAULT 0,
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Transportadora (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  cidade VARCHAR(40) NOT NULL
);
""",
"""
CREATE TABLE IF NOT EXISTS Cliente_Especial (
  id_cliente INT PRIMARY KEY,
  cashback FLOAT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Produto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  quantidade_em_estoque INT NOT NULL,
  valor FLOAT NOT NULL,
  descricao VARCHAR(200) NOT NULL,
  observacoes VARCHAR(200),
  id_vendedor INT,
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Venda (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data_venda DATE NOT NULL,
  hora TIME NOT NULL,
  endereco_destino VARCHAR(100) NOT NULL,
  valor_frete FLOAT NOT NULL,
  id_transportadora INT,
  id_vendedor INT,
  id_cliente INT,
  FOREIGN KEY (id_transportadora) REFERENCES Transportadora(id),
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);
""",
"""
CREATE TABLE IF NOT EXISTS Venda_Produto (
  id_venda INT,
  id_produto INT,
  quantidade INT NOT NULL,
  valor_unitario FLOAT NOT NULL,
  PRIMARY KEY (id_venda, id_produto),
  FOREIGN KEY (id_venda) REFERENCES Venda(id),
  FOREIGN KEY (id_produto) REFERENCES Produto(id)
);
"""
]

# main
cnx = None
cursor = None
try:
    # conectar ao servidor MySQL e criar a database
    cnx = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA
    )
    cursor = cnx.cursor()
    cursor.execute(SQL_CREATE_DB)
    print(f"Banco de dados '{NOME_BANCO}' verificado/criado.")
    
    cursor.close()
    cnx.close()

    cnx = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA,
        database=NOME_BANCO  
    )
    cursor = cnx.cursor()

    print("Iniciando criação de tabelas")

    for tabela_sql in SCHEMA_SQL_TABELAS:
        cursor.execute(tabela_sql)
            
    print("Todas as tabelas foram criadas com sucesso!")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro: Verifique o nome de usuário ou senha.")
    else:
        print(f"Erro ao executar o SQL: {err}")
finally:
    if cursor:
        cursor.close()
    if cnx:
        cnx.close()