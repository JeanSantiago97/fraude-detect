import mysql.connector
from settings import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()
    print(f"Conectado ao banco de dados: {database_name[0]}")
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao MySQL: {err}")
