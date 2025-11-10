# conectar.py
import mysql.connector
from mysql.connector import errorcode
# Precisamos do config.py para as credenciais
from config import HOST, USUARIO, SENHA, NOME_BANCO

def conectar():
    """Tenta conectar ao banco de dados e retorna o objeto de conexão."""
    try:
        con = mysql.connector.connect(
            host=HOST,
            user=USUARIO,
            password=SENHA,
            database=NOME_BANCO
        )
        return con
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
             print(f"❌ Erro: O banco de dados '{NOME_BANCO}' não foi encontrado.")
             print("Execute 'criar_db.py' primeiro.")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             print("❌ Erro: Usuário ou senha do MySQL incorretos.")
        else:
             print(f"❌ Erro de conexão: {err}")
        return None