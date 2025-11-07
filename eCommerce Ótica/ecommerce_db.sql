CREATE DATABASE IF NOT EXISTS ecommerce_oculos_db;
USE ecommerce_oculos_db;


CREATE TABLE IF NOT EXISTS Cargo (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(20) NOT NULL UNIQUE,

  CONSTRAINT chk_cargo_nome CHECK (nome IN ('vendedor', 'gerente', 'CEO'))
);


CREATE TABLE IF NOT EXISTS Cliente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  sexo VARCHAR(1),
  data_de_nascimento DATE NOT NULL,

  CONSTRAINT chk_sexo CHECK (sexo IN ('m', 'f', 'o'))
);


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


CREATE TABLE IF NOT EXISTS Funcionario_Especial (
  id_vendedor INT PRIMARY KEY,
  bonus_total_acumulado FLOAT DEFAULT 0,
  FOREIGN KEY (id_vendedor) REFERENCES Vendedor(id)
);



CREATE TABLE IF NOT EXISTS Transportadora (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(40) NOT NULL,
  cidade VARCHAR(40) NOT NULL
);


CREATE TABLE IF NOT EXISTS Cliente_Especial (
  id_cliente INT PRIMARY KEY,
  cashback FLOAT,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);


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


CREATE TABLE IF NOT EXISTS Venda_Produto (
  id_venda INT,
  id_produto INT,
  quantidade INT NOT NULL,
  valor_unitario FLOAT NOT NULL,
  PRIMARY KEY (id_venda, id_produto),
  FOREIGN KEY (id_venda) REFERENCES Venda(id),
  FOREIGN KEY (id_produto) REFERENCES Produto(id)
);