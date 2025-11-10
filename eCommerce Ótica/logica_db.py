# db_logic.py
# Este ficheiro contém toda a lógica de interação com o banco.

from conectar import conectar
import mysql.connector

# --- Funções que chamam as VIEWS ---
# (Movidas do teu app.py para cá)

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

# --- Funções que chamam as FUNCTIONS SQL ---

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

# --- Funções que chamam as PROCEDURES SQL ---

def chamar_reajuste(percentual):
    con = conectar()
    if not con: return
    cursor = con.cursor()
    try:
        cursor.callproc('Reajuste', (percentual,))
        con.commit() # Reajuste altera dados, precisa de commit
        print(f"✅ Reajuste de {percentual}% aplicado a todos os Vendedores.")
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
        # callproc retorna um iterador para os resultados
        cursor.callproc('Sorteio')
        # Itera sobre os resultados
        for result in cursor.stored_results():
            return result.fetchone() # Retorna o (Nome, Premio)
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
        con.commit() # Venda altera dados, precisa de commit
        print(f"✅ Venda para o Cliente {id_cli} registrada com sucesso!")
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
        # A procedure Estatisticas retorna 4 resultados (SELECTs)
        # Temos que iterar por todos eles
        resultados = []
        for result in cursor.stored_results():
            resultados.append(result.fetchall())
        return resultados
    except mysql.connector.Error as err:
        print(f"Erro ao chamar procedure: {err}")
    finally:
        cursor.close()
        con.close()