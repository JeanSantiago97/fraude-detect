import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="fraude_detector"
        )
        self.cursor = self.conn.cursor()

    def salva_fraude(self, transacao):
        for fraude in transacao["fraudes"]:
            sql = """
            INSERT INTO fraudes (user_id, transaction_id, value, country, fraude, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                transacao["user_id"],
                transacao["transaction_id"],
                transacao["value"],
                transacao["country"],
                fraude,
                transacao["timestamp"]
            )

            self.cursor.execute(sql, values)
        self.conn.commit()

    def __del__(self):
        try:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("Conexão com MySQL fechada corretamente.")
        except Exception as e:
            print(f"Erro ao fechar conexão com MySQL: {e}")

