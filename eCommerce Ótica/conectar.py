import mysql.connector
from config import conexao

def ligar():
    return mysql.connector.connect(**conexao)