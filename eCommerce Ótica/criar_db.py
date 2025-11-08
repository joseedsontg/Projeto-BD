import mysql.connector
from mysql.connector import errorcode
from config import HOST, USUARIO, SENHA

NOME_BANCO = "ecommerce_oculos_db"

# SQL Parte 1: Apenas para criar o banco de dados
SQL_CREATE_DB = f"""
CREATE DATABASE IF NOT EXISTS {NOME_BANCO} 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

#SQL Parte 2: Definições das Funções

SQL_FUNCTION_CALCULA_IDADE = """
CREATE FUNCTION `Calcula_idade`(p_id_cliente INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_data_nascimento DATE;
    DECLARE v_idade INT;
    SELECT data_de_nascimento INTO v_data_nascimento
    FROM Cliente
    WHERE id = p_id_cliente;
    IF v_data_nascimento IS NULL THEN
        RETURN NULL;
    END IF;
    SET v_idade = TIMESTAMPDIFF(YEAR, v_data_nascimento, CURDATE());
    RETURN v_idade;
END
"""

SQL_FUNCTION_SOMA_FRETES = """
CREATE FUNCTION `Soma_fretes`(p_endereco_destino VARCHAR(100))
RETURNS FLOAT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_valor_total_fretes FLOAT DEFAULT 0.0;
    -- CORREÇÃO: Busca na tabela 'Venda'
    SELECT SUM(valor_frete) INTO v_valor_total_fretes
    FROM Venda 
    WHERE endereco_destino = p_endereco_destino;
    IF v_valor_total_fretes IS NULL THEN
        RETURN 0.0;
    END IF;
    RETURN v_valor_total_fretes;
END
"""

SQL_FUNCTION_ARRECADADO = """
CREATE FUNCTION `Arrecadado`(p_data DATE, p_id_vendedor INT)
RETURNS FLOAT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total_arrecadado FLOAT DEFAULT 0.0;
    SELECT SUM(VP.quantidade * VP.valor_unitario) INTO v_total_arrecadado
    FROM Venda AS V
    JOIN Venda_Produto AS VP ON V.id = VP.id_venda
    WHERE V.id_vendedor = p_id_vendedor
      AND V.data_venda = p_data;
    IF v_total_arrecadado IS NULL THEN
        RETURN 0.0;
    END IF;
    RETURN v_total_arrecadado;
END
"""

# (Tabelas + Funções)
SQL_COMANDOS_ESTRUTURA = [
    
    """
    CREATE TABLE IF NOT EXISTS Cliente (
      id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(40) NOT NULL, sexo VARCHAR(1),
      data_de_nascimento DATE NOT NULL, valor_gasto FLOAT DEFAULT 0,
      CONSTRAINT chk_sexo CHECK (sexo IN ('m', 'f', 'o'))
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Vendedor (
      id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(40) NOT NULL,
      causa_social VARCHAR(200) NOT NULL, nota_media FLOAT,
      salario FLOAT NOT NULL DEFAULT 100, valor_vendas FLOAT DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Funcionario_Especial (
      id_vendedor INT PRIMARY KEY, bonus_total_acumulado FLOAT DEFAULT 0,
      FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Transportadora (
      id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(40) NOT NULL, cidade VARCHAR(40) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Cliente_Especial (
      id_cliente INT PRIMARY KEY, cashback FLOAT,
      FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Produto (
      id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(40) NOT NULL,
      quantidade_em_estoque INT NOT NULL, valor FLOAT NOT NULL,
      descricao VARCHAR(200) NOT NULL, observacoes VARCHAR(200),
      id_vendedor INT, FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Venda (
      id INT AUTO_INCREMENT PRIMARY KEY, data_venda DATE NOT NULL, hora TIME NOT NULL,
      endereco_destino VARCHAR(100) NOT NULL, valor_frete FLOAT NOT NULL,
      id_transportadora INT, id_vendedor INT, id_cliente INT,
      FOREIGN KEY (id_transportadora) REFERENCES Transportadora(id),
      FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id),
      FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Venda_Produto (
      id_venda INT, id_produto INT, quantidade INT NOT NULL, valor_unitario FLOAT NOT NULL,
      PRIMARY KEY (id_venda, id_produto),
      FOREIGN KEY (id_venda) REFERENCES Venda(id),
      FOREIGN KEY (id_produto) REFERENCES Produto(id)
    );
    """,
    
    
    "DROP FUNCTION IF EXISTS Calcula_idade",
    SQL_FUNCTION_CALCULA_IDADE,
    
    "DROP FUNCTION IF EXISTS Soma_fretes",
    SQL_FUNCTION_SOMA_FRETES,
    
    "DROP FUNCTION IF EXISTS Arrecadado",
    SQL_FUNCTION_ARRECADADO
]


def criar_banco():
    cnx = None
    cursor = None
  
    
    try:

        cnx = mysql.connector.connect(host=HOST, user=USUARIO, password=SENHA)
        cursor = cnx.cursor()
        cursor.execute(SQL_CREATE_DB)
        print(f"Banco de dados '{NOME_BANCO}' verificado/criado.")
        cursor.close()
        cnx.close()

        cnx = mysql.connector.connect(host=HOST, user=USUARIO, password=SENHA, database=NOME_BANCO)
        cursor = cnx.cursor()
        
        print(f"ℹIniciando criação de Tabelas e Funções no '{NOME_BANCO}'...")
        

        for comando_sql in SQL_COMANDOS_ESTRUTURA:
            cursor.execute(comando_sql)
            
        print("(Revisão 5) Todas as Tabelas e Funções foram criadas com sucesso!")

    except mysql.connector.Error as err:
        if err.errno == 1418:
            print("\n" + "="*50)
            print("ERRO DE PERMISSÃO (1418):")
            print("O MySQL não permitiu que o Python criasse a função.")
            print("Execute isto no seu MySQL Workbench (como root):")
            print("SET GLOBAL log_bin_trust_function_creators = 1;")
            print("="*50 + "\n")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erro: Verifique o nome de usuário ou senha.")
        else:
            print(f"Erro ao executar o SQL: {err}")
    finally:
        if cursor: cursor.close()
        if cnx: cnx.close()

if __name__ == "__main__":
    criar_banco()