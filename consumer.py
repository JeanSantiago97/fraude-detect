from confluent_kafka import Consumer, Producer
import json
from fraud_detector import FraudDetector
from database import Database
from settings import KAFKA_BROKER, KAFKA_TOPIC, KAFKA_FRAUD_TOPIC

class KafkaConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': 'fraude-detector',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([KAFKA_TOPIC])
        self.producer = Producer({'bootstrap.servers': KAFKA_BROKER})
        self.fraud_detector = FraudDetector()
        self.database = Database()

    def publica_fraude(self, transacao):
        tx_json = json.dumps(transacao)
        self.producer.produce(KAFKA_FRAUD_TOPIC, key=str(transacao["user_id"]), value=tx_json)
        self.producer.flush()

    def processa_transacoes(self):
        print("Aguardando transações...")

        while True:
            msg = self.consumer.poll(1.0)  # Espera mensagens do Kafka
            if msg is None:
                continue  # Ignora mensagens nulas

            if msg.error():
                print(f"Erro no Kafka: {msg.error()}")
                continue  # Ignora erros

            msg_value = msg.value()
            if msg_value is None or msg_value.strip() == b"":  # Verifica se está vazio
                print("Mensagem vazia recebida. Ignorando...")
                continue

            try:
                transacao = json.loads(msg_value.decode())  # Converte para JSON
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                continue  # Ignora mensagens corrompidas

            # Se chegou aqui, significa que temos uma transação válida
            fraudes_detectadas = self.fraud_detector.detecta_fraude(transacao)

            if fraudes_detectadas:
                transacao["fraudes"] = fraudes_detectadas
                print(f"🚨 Fraude detectada: {json.dumps(transacao, indent=2)}")
                self.publica_fraude(transacao)
                self.database.salva_fraude(transacao)

if __name__ == "__main__":
    consumer = KafkaConsumer()
    consumer.processa_transacoes()
