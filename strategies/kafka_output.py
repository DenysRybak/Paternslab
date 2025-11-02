import json
from kafka import KafkaProducer


class KafkaOutputStrategy:
    def __init__(self, kafka_server='localhost:9092', topic='your_topic'):
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        self.topic = topic

    def output(self, data):
        for line in data:
            message = json.dumps(line).encode('utf-8')
            self.producer.send(self.topic, message)
        self.producer.flush()


