import pytest
from sqlalchemy.sql import text
from typing import AsyncGenerator

from app import db
from app.db.registry import registry as db_registry

TRUNCATE_QUERY = "TRUNCATE TABLE {tbl_name} CASCADE;"


@pytest.fixture
async def clear_db() -> AsyncGenerator[None, None]:
    yield
    async with db_registry.engine.begin() as conn:
        for db_model in [db.DemoModel, db.Wallet, db.Transaction, db.Event]:
            await conn.execute(text(TRUNCATE_QUERY.format(tbl_name=db_model.__tablename__)))
