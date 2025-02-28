from collections import defaultdict
from datetime import datetime, timedelta


class FraudDetector:
    def __init__(self):
        self.transacoes_usuario = defaultdict(list)
        self.ultimo_valor_usuario = {}
        self.ultima_localizacao_usuario = {}

    def detecta_fraude(self, transacao):
        user_id = transacao["user_id"]
        timestamp = datetime.fromtimestamp(transacao["timestamp"])
        valor = transacao["value"]
        pais = transacao["country"]

        fraudes = []

        # 1. Alta Frequência (menos de 5 minutos entre transações diferentes)
        if self.transacoes_usuario[user_id]:
            for tx in self.transacoes_usuario[user_id]:
                tx_timestamp = datetime.fromtimestamp(tx["timestamp"])
                if (timestamp - tx_timestamp).total_seconds() < 300 and tx["value"] != valor:
                    fraudes.append("Alta Frequência")

        # 2. Alto Valor (mais que o dobro do maior gasto anterior)
        if user_id in self.ultimo_valor_usuario:
            if valor > self.ultimo_valor_usuario[user_id] * 2:
                fraudes.append("Alto Valor")

        self.ultimo_valor_usuario[user_id] = max(valor, self.ultimo_valor_usuario.get(user_id, 0))

        # 3. Outro País (mudança de país em menos de 2 horas)
        if user_id in self.ultima_localizacao_usuario:
            ultima_transacao, ultimo_pais = self.ultima_localizacao_usuario[user_id]
            if ultimo_pais != pais and (timestamp - ultima_transacao).total_seconds() < 7200:
                fraudes.append("Outro País")

        self.ultima_localizacao_usuario[user_id] = (timestamp, pais)
        self.transacoes_usuario[user_id].append(transacao)

        return fraudes
