# Sistema de E-commerce — Projeto de Banco de Dados

> Projeto desenvolvido para a disciplina **Projeto de Banco de Dados**  
> Curso: **Ciência da Computação**  
> Instituição: Universidade Católica de Pernambuco (UNICAP)
> 
> Professor: Jheymesson Apolinario Cavalcanti
>  
> **Integrantes:**
> - Artur Uchôa Simões Barbosa - 00000850742  
> - Gabrielly Gouveia da Silva Feitosa - 00000851368
> - Isabel Lugon Leitão de Oliveira - 00000850648  
> - José Edson Texeira Galdino - 00000850926
> - José Roberval Vieira Gomes Neto - 00000848856

---

**LINK DO FigJam:** https://www.figma.com/board/Cejf1VxIgdxl4q9cIEsvrx/Projeto---Banco-de-Dados-CONCEITUAL---L%C3%93GICO?node-id=0-1&t=akMEl40zTmnXd7id-1

---
## Descrição do Projeto
Este projeto consiste na implementação de um sistema de **E-commerce de uma loja de óculos**, desenvolvido como parte da disciplina **Projeto de Banco de Dados**.  
O objetivo é projetar e implementar um banco de dados relacional utilizando **SQL** e uma **linguagem de apoio** para interação com o sistema.

O sistema permite o gerenciamento completo de **clientes, vendedores, produtos, vendas e transportadoras**, além da aplicação de **regras de negócio** através de **funções, triggers, procedures e views**.

---

## Requisitos e Funcionalidades

### Estrutura Geral
O sistema deve:
- Criar e destruir completamente o banco de dados.
- Incluir pelo menos **20 produtos**, **5 cargos** e **100 clientes ativos**.
- Permitir cadastro, consulta e exclusão de produtos e clientes.

---

### Entidades Principais
- **Clientes:** `id`, `nome`, `idade`, `sexo`, `data_nascimento`.
- **Vendedores:** `id`, `nome`, `causa_social`, `tipo`, `nota_média`.
- **Produtos:** `id`, `nome`, `descrição`, `quantidade_estoque`, `valor`, `observações`.
- **Transportadoras:** `id`, `nome`, `cidade`.
- **Vendas:** registro contendo cliente, vendedor, produtos, transportadora e data/hora da operação.

---

### Regras e Requisitos do Sistema

#### Funções
1. `Calcula_idade` → Recebe o ID do usuário e retorna a idade baseada na data atual.  
2. `Soma_fretes` → Calcula o total de valor de fretes recebidos.  
3. `Arrecadado` → Retorna o valor arrecadado por um vendedor em uma data informada.  

#### Triggers
1. **Bônus salarial:** Se o vendedor vender mais de R$1000,00, um bônus de 5% é adicionado ao salário.  
2. **Cashback cliente:** Se o cliente comprar mais de R$500,00, ganha 2% de cashback.  
3. **Remoção de cashback:** Remove cliente da tabela de “clientes especiais” quando o cashback zera.  

#### Usuários
- **Administrador:** Acesso total.  
- **Gerente:** Pode buscar, editar e deletar registros.  
- **Funcionário:** Pode adicionar registros e consultar vendas.  

#### Views
Criar **3 views** utilizando `JOIN` e `GROUP BY`.

#### Procedures
- `Reajuste`: Aplica reajuste salarial percentual a uma categoria.  
- `Sorteio`: Sorteia um cliente especial e concede voucher de R$100,00 ou R$200,00.  
- `Venda`: Reduz a quantidade de produtos vendidos em 1.  
- `Estatísticas`: Exibe estatísticas como:
  - Produto mais/menos vendido  
  - Vendedor associado ao produto mais vendido  
  - Valor arrecadado com produtos mais e menos vendidos  
  - Mês de maior e menor venda  

---

## Constraints
- **Sexo:** Deve ser `'m'`, `'f'` ou `'o'`.  

---

## Tecnologias Utilizadas
- **Banco de Dados:** SQL 
- **Linguagem de Apoio:** Python  
- **Ferramentas:** MySQL Workbench, VS Code, FigJam, GitHub.

---

## Conceitos Aplicados
- Modelagem de dados  
- Criação e manipulação de tabelas  
- Consultas com `JOIN`, `GROUP BY` e `HAVING`  
- Criação de **triggers**, **views**, **funções** e **procedimentos armazenados**  
- Controle de acesso e usuários com diferentes níveis de permissão  

---

## Licença
Este projeto é de uso educacional, desenvolvido apenas para fins acadêmicos.

---

