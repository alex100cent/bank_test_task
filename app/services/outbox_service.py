from sqlalchemy import select

from app.db import Event
from app.db.registry import registry
from app.services.kafka_service import kafka_service


async def outbox_send_service():
    await registry.setup()
    await kafka_service.setup()
    async with registry.session() as session:
        stmt = select(Event).where(Event.status == Event.NEW)
        events = (await session.execute(stmt)).scalars().all()
        for event in events:
            await kafka_service.send_message_to_kafka(event.topic_name, event.body)
            event.status = 1
        await session.commit()
    await registry.close()
