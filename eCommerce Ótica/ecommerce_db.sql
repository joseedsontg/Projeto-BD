CREATE DATABASE IF NOT EXISTS ecommerce_oculos_db;
USE ecommerce_oculos_db;


CREATE TABLE Cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  sexo VARCHAR(1),
  data_de_nascimento DATE NOT NULL,
  valor_gasto FLOAT DEFAULT 0,
  CONSTRAINT chk_sexo CHECK (sexo IN ('m', 'f', 'o'))
);

CREATE TABLE Vendedor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  causa_social VARCHAR(200) NOT NULL,
  nota_media FLOAT,
  salario FLOAT NOT NULL DEFAULT 100,
  valor_vendas FLOAT DEFAULT 0
);

CREATE TABLE Funcionario_Especial (
  id_vendedor INT PRIMARY KEY,
  bonus_total_acumulado FLOAT DEFAULT 0,
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);

CREATE TABLE Transportadora (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  cidade VARCHAR(40) NOT NULL
);

CREATE TABLE Cliente_Especial (
  id_cliente INT PRIMARY KEY,
  cashback FLOAT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);

CREATE TABLE Produto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  quantidade_em_estoque INT NOT NULL,
  valor FLOAT NOT NULL,
  descricao VARCHAR(200) NOT NULL,
  observacoes VARCHAR(200),
  id_vendedor INT,
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);

/* Corrigido: Adicionadas as colunas de 'Transporte_Venda' aqui.
   Agora a Venda sabe o seu destino e frete.
*/
CREATE TABLE Venda (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data_venda DATE NOT NULL,
  hora TIME NOT NULL,
  endereco_destino VARCHAR(100) NOT NULL, /* <-- Movido para cá */
  valor_frete FLOAT NOT NULL,             /* <-- Movido para cá */
  id_transportadora INT,
  id_vendedor INT,
  id_cliente INT,
  FOREIGN KEY (id_transportadora) REFERENCES Transportadora(id),
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);

/* Removido: Tabela 'Transporte_Venda' (redundante).
   As suas informações estão agora em 'Venda'.
*/

CREATE TABLE Venda_Produto (
  id_venda INT,
  id_produto INT,
  quantidade INT NOT NULL,
  valor_unitario FLOAT NOT NULL,
  PRIMARY KEY (id_venda, id_produto),
  FOREIGN KEY (id_venda) REFERENCES Venda(id),
  FOREIGN KEY (id_produto) REFERENCES Produto(id)
);

CREATE FUNCTION `Calcula_idade`(p_id_cliente INT)(
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
END);

CREATE FUNCTION `Soma_fretes`(p_endereco_destino VARCHAR(100))(
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
END);

CREATE FUNCTION `Arrecadado`(p_data DATE, p_id_vendedor INT)(
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
END);

-- VIEWS

-- 1 View: Total gasto por cliente
CREATE OR REPLACE VIEW vw_total_gasto_por_cliente AS
SELECT 
    C.id AS id_cliente,
    C.nome AS nome_cliente,
    SUM(VP.quantidade * VP.valor_unitario) AS total_gasto
FROM Cliente C
JOIN Venda V ON C.id = V.id_cliente
JOIN Venda_Produto VP ON V.id = VP.id_venda
GROUP BY C.id, C.nome;

-- 2 View: Total vendido por vendedor
CREATE OR REPLACE VIEW vw_total_vendido_por_vendedor AS
SELECT 
    Vd.id AS id_vendedor,
    Vd.nome AS nome_vendedor,
    SUM(VP.quantidade * VP.valor_unitario) AS total_vendido
FROM Vendedor Vd
JOIN Venda Ve ON Vd.id = Ve.id_vendedor
JOIN Venda_Produto VP ON Ve.id = VP.id_venda
GROUP BY Vd.id, Vd.nome;

-- 2 View: Produtos mais vendidos
CREATE OR REPLACE VIEW vw_produtos_mais_vendidos AS
SELECT 
    P.id AS id_produto,
    P.nome AS nome_produto,
    SUM(VP.quantidade) AS total_vendido
FROM Produto P
JOIN Venda_Produto VP ON P.id = VP.id_produto
GROUP BY P.id, P.nome
ORDER BY total_vendido DESC;