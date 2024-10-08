from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from starlette import status
from uuid import UUID

from app.models import WalletCreateScheme, TransactionCreateScheme, TransactionGetMoneyScheme
from app.services.wallet_service import (
    create_wallet_service,
    get_wallets_by_uuid_service,
    create_transaction_service,
    get_money_service,
)

router = APIRouter()


@router.post("/wallets")
async def create_wallet(request: WalletCreateScheme):
    return ORJSONResponse(
        jsonable_encoder(await create_wallet_service(request)),
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/user/{user_uid}/wallets")
async def get_wallets_by_user_id(user_uid: UUID):
    return ORJSONResponse(
        jsonable_encoder(await get_wallets_by_uuid_service(user_uid=user_uid)),
        status_code=status.HTTP_200_OK,
    )


@router.get("/wallets/{wallet_id}")
async def get_wallet_by_wallet_id(wallet_id: UUID):
    return ORJSONResponse(
        jsonable_encoder(await get_wallets_by_uuid_service(wallet_uid=wallet_id)),
        status_code=status.HTTP_200_OK,
    )


@router.put("/wallets/transactions")
async def create_wallet_transaction(request: TransactionCreateScheme):
    result = await create_transaction_service(request)
    if result.is_done:
        return ORJSONResponse(
            jsonable_encoder(result),
            status_code=status.HTTP_201_CREATED,
        )
    else:
        return ORJSONResponse(
            jsonable_encoder(result),
            status_code=status.HTTP_200_OK,
        )


@router.post("/wallets/send_gift")
async def send_gift(request: TransactionGetMoneyScheme):
    return ORJSONResponse(
        jsonable_encoder(await get_money_service(request)),
        status_code=status.HTTP_200_OK,
    )
