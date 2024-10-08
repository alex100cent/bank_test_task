import pytest
from sqlalchemy import select
from unittest.mock import patch, AsyncMock

from app.db import Event
from app.db.registry import registry as db_registry
from app.services.outbox_service import outbox_send_service
from tests.factories.db import EventModelFactory


@pytest.mark.usefixtures("clear_db")
@patch("app.services.outbox_service.send_message_to_kafka", new_callable=AsyncMock)
async def test_outbox_send_task(mock_send_message_to_kafka) -> None:
    event_before = await EventModelFactory(status=0)

    await outbox_send_service()

    async with db_registry.session() as session:
        event_after = (
            (await session.execute(select(Event).where(Event.id == event_before.id)))
            .scalars()
            .one()
        )
    mock_send_message_to_kafka.assert_called_once()
    assert event_after.status == 1


@pytest.mark.usefixtures("clear_db")
@patch("app.services.outbox_service.send_message_to_kafka", new_callable=AsyncMock)
async def test_outbox_send_task_no_events(mock_send_message_to_kafka) -> None:
    await outbox_send_service()
    mock_send_message_to_kafka.assert_not_called()
