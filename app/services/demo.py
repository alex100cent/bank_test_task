import uuid

from fastapi.exceptions import HTTPException
from sqlalchemy import select

from app.db import DemoModel
from app.db.registry import registry
from app.models import CreateDemoScheme, DemoScheme


async def get_demo_list() -> list[DemoScheme]:
    async with registry.session() as session:
        result = (await session.execute(select(DemoModel))).scalars().all()

        if not result:
            raise HTTPException(status_code=404)

        return [DemoScheme.from_orm(row) for row in result]


async def create_demo(model: CreateDemoScheme) -> DemoScheme:
    async with registry.session() as session:
        demo = DemoModel(uid=uuid.uuid4(), type_=model.type_)
        session.add(demo)
        await session.commit()

    return DemoScheme.from_orm(demo)
