from enum import Enum


class KafkaTopic(Enum):
    TRANSACTION_CREATE = "transaction_create"


class KafkaProducer(Enum):
    TRANSACTION_PRODUCER = "transaction_producer"
