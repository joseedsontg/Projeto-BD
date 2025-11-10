from conectar import conectar
import mysql.connector

def get_view_total_gasto():
    con = conectar()
    if not con: return
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_total_gasto_por_cliente")
    resultados = cursor.fetchall()
    cursor.close()
    con.close()
    return resultados

def get_view_total_vendido():
    con = conectar()
    if not con: return
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_total_vendido_por_vendedor")
    resultados = cursor.fetchall()
    cursor.close()
    con.close()
    return resultados

def get_view_produtos_mais_vendidos():
    con = conectar()
    if not con: return
    cursor = con.cursor()
    cursor.execute("SELECT * FROM vw_produtos_mais_vendidos")
    resultados = cursor.fetchall()
    cursor.close()
    con.close()
    return resultados

def chamar_calcula_idade(id_cliente):
    con = conectar()
    if not con: return None
    cursor = con.cursor()
    try:
        cursor.execute("SELECT Calcula_idade(%s)", (id_cliente,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return None
    except mysql.connector.Error as err:
        print(f"Erro ao chamar função: {err}")
        return None
    finally:
        cursor.close()
        con.close()

def chamar_soma_fretes(destino):
    con = conectar()
    if not con: return None
    cursor = con.cursor()
    try:
        cursor.execute("SELECT Soma_fretes(%s)", (destino,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return 0.0
    except mysql.connector.Error as err:
        print(f"Erro ao chamar função: {err}")
        return None
    finally:
        cursor.close()
        con.close()

def chamar_arrecadado(data, id_vendedor):
    con = conectar()
    if not con: return None
    cursor = con.cursor()
    try:
        cursor.execute("SELECT Arrecadado(%s, %s)", (data, id_vendedor))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        return 0.0
    except mysql.connector.Error as err:
        print(f"Erro ao chamar função: {err}")
        return None
    finally:
        cursor.close()
        con.close()

def chamar_reajuste(percentual):
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        cursor.callproc('Reajuste', (percentual,))
        con.commit() 
        print(f"Reajuste de {percentual}% aplicado a todos os Vendedores.")
    except mysql.connector.Error as err:
        print(f"Erro ao chamar procedure: {err}")
    finally:
        cursor.close()
        con.close()

def chamar_sorteio():
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        cursor.callproc('Sorteio')
        for result in cursor.stored_results():
            return result.fetchone() 
    except mysql.connector.Error as err:
        print(f"Erro ao chamar procedure: {err}")
    finally:
        cursor.close()
        con.close()

def chamar_realizar_venda(id_cli, id_vend, id_trans, end, id_prod):
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        cursor.callproc('Realizar_Venda', (id_cli, id_vend, id_trans, end, id_prod))
        con.commit() 
        print(f"Venda para o Cliente {id_cli} registrada com sucesso!")
        print("ℹ  Triggers de bônus e cashback podem ter sido disparados.")
    except mysql.connector.Error as err:
        print(f"Erro ao chamar procedure: {err}")
    finally:
        cursor.close()
        con.close()

def chamar_estatisticas():
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        cursor.callproc('Estatisticas')
        resultados = []
        for result in cursor.stored_results():
            resultados.append(result.fetchall())
        return resultados
    except mysql.connector.Error as err:
        print(f"Erro ao chamar procedure: {err}")
    finally:
        cursor.close()
        con.close()

def cadastrar_cliente(nome, sexo, data_nasc):
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        sql = "INSERT INTO Cliente (nome, sexo, data_de_nascimento) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, sexo, data_nasc))
        con.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar cliente: {err}")
    finally:
        cursor.close()
        con.close()

def cadastrar_produto(nome, estoque, valor, desc, id_vend):
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        sql = """
        INSERT INTO Produto (nome, quantidade_em_estoque, valor, descricao, id_vendedor)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, estoque, valor, desc, id_vend))
        con.commit()
        print(f"Produto '{nome}' cadastrado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar produto: {err}")
    finally:
        cursor.close()
        con.close()