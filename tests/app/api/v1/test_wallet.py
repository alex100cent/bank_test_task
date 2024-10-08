import pytest
import uuid
from fastapi.encoders import jsonable_encoder
from starlette import status
from typing import TYPE_CHECKING

from app.main import app
from tests.factories.db import WalletModelFactory
from tests.factories.schemes import CreateWalletSchemeFactory

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet(
        client: "AsyncClient",
) -> None:
    payload = CreateWalletSchemeFactory.build()

    response = await client.post(
        app.url_path_for(
            "create_wallet",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_uid"] == str(payload.user_uid)


@pytest.mark.parametrize("amount", [1, 2])
@pytest.mark.usefixtures("clear_db")
async def test_get_wallets_by_user_id(
        client: "AsyncClient",
        amount: int,
) -> None:
    user_uid = uuid.uuid4()
    expected_data = []
    for _ in range(amount):
        expected_data.append(await WalletModelFactory.create(user_uid=user_uid))

    response = await client.get(
        app.url_path_for("get_wallets_by_user_id", user_uid=user_uid),
    )

    assert response.status_code == status.HTTP_200_OK
    for data in response.json():
        assert data["user_uid"] == str(user_uid)


@pytest.mark.usefixtures("clear_db")
async def test_get_wallets_by_user_id_not_found(
        client: "AsyncClient",
) -> None:
    response = await client.get(
        app.url_path_for(
            "get_wallets_by_user_id",
            user_uid=uuid.uuid4(),
        ),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("clear_db")
async def test_get_wallet_by_wallet_id(
        client: "AsyncClient",
) -> None:
    wallet = await WalletModelFactory.create()

    response = await client.get(
        app.url_path_for(
            "get_wallet_by_wallet_id",
            wallet_id=str(wallet.id),
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == str(wallet.id)


@pytest.mark.usefixtures("clear_db")
async def test_get_wallet_by_wallet_id_not_found(
        client: "AsyncClient",
) -> None:
    response = await client.get(
        app.url_path_for(
            "get_wallet_by_wallet_id",
            wallet_id=uuid.uuid4(),
        ),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
