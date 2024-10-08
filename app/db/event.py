import uuid
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, JSON
from sqlalchemy import DateTime, func
from sqlalchemy.sql.sqltypes import UUID, Integer, String

from .registry import registry
from ..constants import KafkaTopic, KafkaProducer

Base = registry.base


class Event(Base):  # type: ignore
    __tablename__ = "event"

    NEW = 0

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_name = Column(String(254), nullable=False)
    producer = Column(String(254), nullable=False)
    body = Column(JSON, nullable=False)
    status = Column(Integer, nullable=False, default=NEW)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)

    @classmethod
    def create(cls, body: dict) -> "Event":
        return cls(
            topic_name=KafkaTopic.TRANSACTION_CREATE.value,
            producer=KafkaProducer.TRANSACTION_PRODUCER.value,
            body=jsonable_encoder(body),
        )
