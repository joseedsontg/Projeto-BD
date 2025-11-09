import mysql.connector
from mysql.connector import errorcode
from config import HOST, USUARIO, SENHA

NOME_BANCO = "ecommerce_oculos_db"

# SQL Parte 1: Apenas para criar o banco de dados
SQL_CREATE_DB = f"""
CREATE DATABASE IF NOT EXISTS {NOME_BANCO} 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""

# SQL Parte 2: Definições das Funções
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

# ============================
# Estrutura do Banco
# ============================

SQL_COMANDOS_ESTRUTURA = [
    # Tabelas
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

    # Funções
    "DROP FUNCTION IF EXISTS Calcula_idade",
    SQL_FUNCTION_CALCULA_IDADE,

    "DROP FUNCTION IF EXISTS Soma_fretes",
    SQL_FUNCTION_SOMA_FRETES,

    "DROP FUNCTION IF EXISTS Arrecadado",
    SQL_FUNCTION_ARRECADADO,

    # ================================
    # VIEWS
    # ================================
    "DROP VIEW IF EXISTS vw_total_gasto_por_cliente",
    """
    CREATE VIEW vw_total_gasto_por_cliente AS
    SELECT 
        C.id AS id_cliente,
        C.nome AS nome_cliente,
        SUM(VP.quantidade * VP.valor_unitario) AS total_gasto
    FROM Cliente C
    JOIN Venda V ON C.id = V.id_cliente
    JOIN Venda_Produto VP ON V.id = VP.id_venda
    GROUP BY C.id, C.nome;
    """,

    "DROP VIEW IF EXISTS vw_total_vendido_por_vendedor",
    """
    CREATE VIEW vw_total_vendido_por_vendedor AS
    SELECT 
        Vd.id AS id_vendedor,
        Vd.nome AS nome_vendedor,
        SUM(VP.quantidade * VP.valor_unitario) AS total_vendido
    FROM Vendedor Vd
    JOIN Venda Ve ON Vd.id = Ve.id_vendedor
    JOIN Venda_Produto VP ON Ve.id = VP.id_venda
    GROUP BY Vd.id, Vd.nome;
    """,

    "DROP VIEW IF EXISTS vw_produtos_mais_vendidos",
    """
    CREATE VIEW vw_produtos_mais_vendidos AS
    SELECT 
        P.id AS id_produto,
        P.nome AS nome_produto,
        SUM(VP.quantidade) AS total_vendido
    FROM Produto P
    JOIN Venda_Produto VP ON P.id = VP.id_produto
    GROUP BY P.id, P.nome
    ORDER BY total_vendido DESC;
    """

    #Procedimentos

    "DROP PROCEDURE IF EXISTS Reajuste",
    """
    CREATE PROCEDURE Reajuste(IN p_percentual FLOAT)
    BEGIN
        UPDATE Vendedor
        SET salario = salario + (salario * (p_percentual / 100));
    END
    """

    "DROP PROCEDURE IF EXISTS Sorteio",
    """
    CREATE PROCEDURE Sorteio()
    BEGIN
        DECLARE v_id_cliente_sorteado INT;
        DECLARE v_nome_cliente_sorteado VARCHAR(40);
        DECLARE v_eh_cliente_especial INT DEFAULT 0;
        DECLARE v_valor_premio FLOAT;

        -- 1. Sorteia UM cliente aleatório
        SELECT id, nome INTO v_id_cliente_sorteado, v_nome_cliente_sorteado 
        FROM Cliente 
        ORDER BY RAND() 
        LIMIT 1;

        -- 2. Verifica se ele é especial
        SELECT COUNT(*) INTO v_eh_cliente_especial 
        FROM Cliente_Especial 
        WHERE id_cliente = v_id_cliente_sorteado;

        -- 3. Define o prêmio
        IF v_eh_cliente_especial > 0 THEN
            SET v_valor_premio = 200.00;
        ELSE
            SET v_valor_premio = 100.00;
        END IF;

        -- 4. Mostra o resultado
        SELECT v_nome_cliente_sorteado AS 'Cliente Sorteado', 
               v_valor_premio AS 'Valor do Voucher (R$)';
    END
    """

    "DROP PROCEDURE IF EXISTS Realizar_Venda",
    """
    CREATE PROCEDURE Realizar_Venda(
        IN p_id_cliente INT,
        IN p_id_vendedor INT,
        IN p_id_transportadora INT,
        IN p_endereco_entrega VARCHAR(100),
        IN p_id_produto INT
    )
    BEGIN
        DECLARE v_preco_atual FLOAT;
        DECLARE v_id_nova_venda INT;

        -- 1. Obtém o preço atual do produto
        SELECT valor INTO v_preco_atual FROM Produto WHERE id = p_id_produto;

        -- 2. Registra a venda
        INSERT INTO Venda (data_venda, hora, endereco_destino, valor_frete, id_transportadora, id_vendedor, id_cliente)
        VALUES (CURDATE(), CURTIME(), p_endereco_entrega, 50.00, p_id_transportadora, p_id_vendedor, p_id_cliente);

        -- 3. Recupera o ID da venda recém-criada
        SET v_id_nova_venda = LAST_INSERT_ID();

        -- 4. Registra o item na venda (Quantidade fixa = 1)
        INSERT INTO Venda_Produto (id_venda, id_produto, quantidade, valor_unitario)
        VALUES (v_id_nova_venda, p_id_produto, 1, v_preco_atual);

        -- 5. Reduz em 1 o estoque
        UPDATE Produto 
        SET quantidade_em_estoque = quantidade_em_estoque - 1
        WHERE id = p_id_produto;
    END
    """

    "DROP PROCEDURE IF EXISTS Estatisticas",
    """
    CREATE PROCEDURE Estatisticas()
    BEGIN
        -- 1. Produto MAIS vendido, Vendedor associado e Valor ganho
        SELECT 'MAIS VENDIDO' AS Categoria,
               P.nome AS Produto,
               Vd.nome AS 'Vendedor Associado',
               SUM(VP.quantidade) AS 'Qtd Total',
               SUM(VP.quantidade * VP.valor_unitario) AS 'Valor Ganho Total'
        FROM Venda_Produto VP
        JOIN Produto P ON VP.id_produto = P.id
        JOIN Venda V ON VP.id_venda = V.id
        JOIN Vendedor Vd ON V.id_vendedor = Vd.id
        GROUP BY P.id, P.nome, Vd.nome
        ORDER BY SUM(VP.quantidade) DESC
        LIMIT 1;

        -- 2. Mês de MAIOR e MENOR venda do produto MAIS vendido
        SELECT 'MESES (Mais Vendido)' AS Categoria,
               MONTH(V.data_venda) AS Mes,
               SUM(VP.quantidade) AS Qtd_no_Mes
        FROM Venda_Produto VP
        JOIN Venda V ON VP.id_venda = V.id
        WHERE VP.id_produto = (
            SELECT id_produto FROM Venda_Produto GROUP BY id_produto ORDER BY SUM(quantidade) DESC LIMIT 1
        )
        GROUP BY MONTH(V.data_venda)
        ORDER BY Qtd_no_Mes DESC; -- O primeiro é o mês de maior venda, o último é o de menor.

        -- 3. Produto MENOS vendido e Valor ganho
        SELECT 'MENOS VENDIDO' AS Categoria,
               P.nome AS Produto,
               '-' AS 'Vendedor Associado',
               SUM(VP.quantidade) AS 'Qtd Total',
               SUM(VP.quantidade * VP.valor_unitario) AS 'Valor Ganho Total'
        FROM Venda_Produto VP
        JOIN Produto P ON VP.id_produto = P.id
        GROUP BY P.id, P.nome
        ORDER BY SUM(VP.quantidade) ASC
        LIMIT 1;

         -- 4. Mês de MAIOR e MENOR venda do produto MENOS vendido
        SELECT 'MESES (Menos Vendido)' AS Categoria,
               MONTH(V.data_venda) AS Mes,
               SUM(VP.quantidade) AS Qtd_no_Mes
        FROM Venda_Produto VP
        JOIN Venda V ON VP.id_venda = V.id
        WHERE VP.id_produto = (
            SELECT id_produto FROM Venda_Produto GROUP BY id_produto ORDER BY SUM(quantidade) ASC LIMIT 1
        )
        GROUP BY MONTH(V.data_venda)
        ORDER BY Qtd_no_Mes DESC;
    END
    """
    
]

# ============================
# Função principal
# ============================

def criar_banco():
    cnx = None
    cursor = None
    
    try:
        # Cria o banco
        cnx = mysql.connector.connect(host=HOST, user=USUARIO, password=SENHA)
        cursor = cnx.cursor()
        cursor.execute(SQL_CREATE_DB)
        print(f"Banco de dados '{NOME_BANCO}' verificado/criado.")
        cursor.close()
        cnx.close()

        # Conecta ao banco recém-criado
        cnx = mysql.connector.connect(host=HOST, user=USUARIO, password=SENHA, database=NOME_BANCO)
        cursor = cnx.cursor()

        print(f"ℹ️ Iniciando criação de Tabelas, Funções e Views no '{NOME_BANCO}'...")

        for comando_sql in SQL_COMANDOS_ESTRUTURA:
            cursor.execute(comando_sql)

        print("✅ Todas as Tabelas, Funções e Views foram criadas com sucesso!")

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
