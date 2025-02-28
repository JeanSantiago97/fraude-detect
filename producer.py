from confluent_kafka import Producer
import json
from gen_transaction import TransactionGenerator
from dataclasses import asdict
from time import sleep
from settings import KAFKA_BROKER, KAFKA_TOPIC  # Configurações do Kafka

class KafkaProducer:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': KAFKA_BROKER})
        self.generator = TransactionGenerator(trans_per_sec=5)

    def delivery_report(self, err, msg):
        if err:
            print(f"Erro ao enviar mensagem: {err}")
        else:
            print(f"Mensagem enviada: {msg.value().decode()}")

    def produce_transactions(self):
        for tx in self.generator.generate_transactions():
            tx_json = json.dumps(asdict(tx))
            self.producer.produce(KAFKA_TOPIC, key=str(tx.user_id), value=tx_json, callback=self.delivery_report)
            self.producer.flush()
            sleep(0.1)

if __name__ == "__main__":
    producer = KafkaProducer()
    producer.produce_transactions()
