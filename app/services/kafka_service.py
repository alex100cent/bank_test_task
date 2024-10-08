from json import dumps

from aiokafka import AIOKafkaProducer

from app.config import kafka


class KafkaService:
    producer: AIOKafkaProducer

    async def setup(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=kafka.bootstrap_servers,
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )
        await self.producer.start()

    async def send_message_to_kafka(self, topic_name: str, msg: dict):
        await self.producer.send(topic_name, value=msg)


kafka_service = KafkaService()
