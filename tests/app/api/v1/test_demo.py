from typing import TYPE_CHECKING

import pytest
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.main import app
from tests.factories.db import DemoModelFactory
from tests.factories.schemes import CreateDemoSchemeFactory

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.usefixtures("clear_db")
async def test_create_demo(
        client: "AsyncClient",
) -> None:
    payload = CreateDemoSchemeFactory.build()

    response = await client.post(
        app.url_path_for(
            "create_one_demo",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["type"] == payload.type_


@pytest.mark.parametrize("amount", [1, 2])
@pytest.mark.usefixtures("clear_db")
async def test_get_demo_list(
        client: "AsyncClient",
        amount: int,
) -> None:
    expected_data = []
    for i in range(amount):
        expected_data.append(await DemoModelFactory.create())

    response = await client.get(
        app.url_path_for(
            "retrieve_demo_list",
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"uid": str(expected.uid), "type": expected.type_} for expected in expected_data
    ]
