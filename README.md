# Detecção de Fraudes em Transações Financeiras com Kafka

Este projeto faz parte de um trabalho de pós-graduação do MIT em Engenharia de Dados, realizado pelo Instituto Infnet. A proposta é desenvolver uma aplicação que processe transações financeiras em tempo real utilizando Apache Kafka, identificando atividades suspeitas e fraudes com base em regras específicas, sem a utilização de Machine Learning.

## Objetivo

Desenvolver um módulo de detecção de fraudes em transações financeiras, onde:
- As transações são geradas em tempo real e enviadas para um tópico Kafka.
- Um consumidor processa as mensagens, aplicando regras de fraude para identificar atividades suspeitas.
- As fraudes detectadas são publicadas em um novo tópico Kafka e armazenadas em um banco de dados (MySQL).

## Regras de Fraude

A detecção de fraude é baseada nas seguintes regras:
- **Alta Frequência:** Um usuário realizou duas transações com valores diferentes em um intervalo inferior a 5 minutos.
- **Alto Valor:** Um usuário realizou uma transação que excede o dobro do maior valor gasto em transações anteriores.
- **Outro País:** Um usuário fez uma transação em um país diferente menos de 2 horas após uma transação anterior.

## Tecnologias Utilizadas

- **Apache Kafka:** Sistema de mensageria para processamento de dados em tempo real.
- **Python (confluent-kafka):** Implementação dos produtores e consumidores Kafka.
- **MySQL:** Banco de dados para armazenamento dos dados de transações suspeitas.
- **Docker:** Para execução isolada e simplificada do Kafka e Zookeeper.
- **WampServer:** Ambiente para o MySQL.

## Estrutura do Projeto

```
fraude-detect/
├── consumer.py             # Consumidor Kafka que processa as transações e detecta fraudes
├── producer.py             # Produtor Kafka que gera e envia transações para o Kafka
├── fraud_detector.py       # Módulo que implementa as regras de detecção de fraude
├── database.py             # Módulo para persistência de fraudes no MySQL
├── settings.py             # Configurações do Kafka e do banco de dados
└── gen_transaction.py      # Gerador de transações (dados simulados)
```

## Configuração do Ambiente

### Kafka e Zookeeper (Docker)

#### Configuração
```sh
# 1️⃣ Iniciar o Zookeeper
docker run -d --name kafka --link zookeeper:zookeeper -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 wurstmeister/kafka

# 2️⃣ Iniciar o Kafka
docker exec -it kafka kafka-topics.sh --create --topic transacoes --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# 3️⃣ Criar o tópico 'transacoes'
docker exec -it kafka kafka-topics.sh --create --topic transacoes --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# 4️⃣ Criar o tópico 'fraudes'
docker exec -it kafka kafka-topics.sh --create --topic fraudes --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

#### Testes
```sh
# 1️⃣ Listar os tópicos criados
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092

# 2️⃣ Enviar mensagens manualmente para 'transacoes'
docker exec -it kafka kafka-console-producer.sh --broker-list localhost:9092 --topic transacoes

# 3️⃣ Consumir mensagens do tópico 'transacoes'
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic transacoes --from-beginning

# 4️⃣ Consumir mensagens do tópico 'fraudes'
docker exec -it kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic fraudes --from-beginning
```

### Banco de Dados (MySQL)

```sql
-- Criar banco de dados
CREATE DATABASE fraude_detector;

-- Usar banco de dados
USE fraude_detector;

-- Criar tabela para armazenar fraudes
CREATE TABLE fraudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    value FLOAT NOT NULL,
    country VARCHAR(50) NOT NULL,
    fraude VARCHAR(50) NOT NULL,
    timestamp DATETIME NOT NULL
);

-- Consultar todas as fraudes detectadas
SELECT * FROM fraudes;
```

## Execução do Projeto

1. **Inicie os serviços do Kafka e Zookeeper (Docker):**

   - Execute os comandos listados na seção *Kafka e Zookeeper*.

2. **Crie os tópicos **``transacoes e fraudes``**:**

   - Utilize os comandos indicados para criação dos tópicos.

3. **Execute o Produtor Kafka:**

   - No terminal, execute:
     ```sh
     python producer.py
     ```
   - O produtor gera transações continuamente e envia mensagens para o tópico `transacoes`.

4. **Execute o Consumidor Kafka:**

   - Em outro terminal, execute:
     ```sh
     python consumer.py
     ```
   - O consumidor lê as mensagens, aplica as regras de fraude e, se detectar fraude, publica os dados no tópico `fraudes` e os armazena no MySQL.

5. **Verifique os Dados:**

   - Utilize o phpMyAdmin ou o terminal do MySQL para consultar a tabela `fraudes`:
     ```sql
     SELECT * FROM fraudes;
     ```

## Considerações Finais

Este projeto demonstra uma arquitetura robusta para detecção de fraudes em tempo real. A solução integra Apache Kafka para transmissão e processamento de mensagens, Python para aplicação lógica e MySQL para persistência dos dados, proporcionando uma base sólida para o desenvolvimento de sistemas de monitoramento e análise de transações financeiras.

**Trabalho de Pós Graduação MIT - Engenharia de Dados - Instituto Infnet**

---
