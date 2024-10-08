import pytest
import uuid
from fastapi.encoders import jsonable_encoder
from starlette import status
from typing import TYPE_CHECKING

from app.main import app
from app.models import TransactionCreateScheme
from tests.factories.db import WalletModelFactory
from tests.factories.schemes import TransactionCreateSchemeFactory

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction(
        client: "AsyncClient",
) -> None:
    payload: TransactionCreateScheme = TransactionCreateSchemeFactory.build(amount=100.55)
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.sender_wallet_id, balance=500, is_active=True
    )
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.receiver_wallet_id, balance=100, is_active=True
    )

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == str(payload.id)
    assert response.json()["description"] == ""
    assert response.json()["is_done"]


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction_not_enough_money(
        client: "AsyncClient",
) -> None:
    payload: TransactionCreateScheme = TransactionCreateSchemeFactory.build(amount=100.55)
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.sender_wallet_id, balance=100, is_active=True
    )
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.receiver_wallet_id, balance=100, is_active=True
    )

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction_idempotency(
        client: "AsyncClient",
) -> None:
    payload = TransactionCreateSchemeFactory.build(amount=100.55)
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.sender_wallet_id, balance=500, is_active=True
    )
    await WalletModelFactory.create(
        user_uid=uuid.uuid4(), id=payload.receiver_wallet_id, balance=100, is_active=True
    )

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == str(payload.id)
    assert response.json()["description"] == ""
    assert response.json()["is_done"]

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_200_OK
    assert not response.json()["is_done"]
    assert response.json()["description"] != ""


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction_one_user_different_wallets(
        client: "AsyncClient",
) -> None:
    user_uid = uuid.uuid4()
    payload = TransactionCreateSchemeFactory.build(amount=100.55)
    await WalletModelFactory.create(
        user_uid=user_uid, id=payload.sender_wallet_id, balance=500, is_active=True
    )
    await WalletModelFactory.create(
        user_uid=user_uid, id=payload.receiver_wallet_id, balance=100, is_active=True
    )

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] == str(payload.id)
    assert response.json()["description"] == ""
    assert response.json()["is_done"]


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction_one_wallet(
        client: "AsyncClient",
) -> None:
    sender_wallet_id = uuid.uuid4()
    payload = TransactionCreateSchemeFactory.build(
        amount=100.55, sender_wallet_id=sender_wallet_id, receiver_wallet_id=sender_wallet_id
    )
    await WalletModelFactory.create(id=sender_wallet_id, balance=500, is_active=True)

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.usefixtures("clear_db")
async def test_create_wallet_transaction_wallet_not_found(
        client: "AsyncClient",
) -> None:
    payload = TransactionCreateSchemeFactory.build()

    response = await client.put(
        app.url_path_for(
            "create_wallet_transaction",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
