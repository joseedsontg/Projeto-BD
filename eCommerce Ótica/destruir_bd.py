import mysql.connector
from config import HOST, USUARIO, SENHA

NOME_BANCO = "ecommerce_oculos_db"

cnx = None
cursor = None
try:

    cnx = mysql.connector.connect(
        host=HOST,
        user=USUARIO,
        password=SENHA
    )
    cursor = cnx.cursor()
    
    cursor.execute(f"DROP DATABASE IF EXISTS {NOME_BANCO}")
    
    print(f"Banco de dados '{NOME_BANCO}' destruído com sucesso!")

except mysql.connector.Error as err:
    print(f"Erro: {err}")
finally:
    if cursor:
        cursor.close()
    if cnx:
        cnx.close()