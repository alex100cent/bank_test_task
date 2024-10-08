import json
import uuid
from datetime import datetime, timezone
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.cache_utils.cache_utils import cache_service
from app.db import Wallet, Transaction
from app.db.event import Event
from app.db.registry import registry
from app.models import (
    WalletCreateScheme,
    WalletScheme,
    TransactionCreateScheme,
    TransactionGetMoneyScheme,
    TransactionResponseScheme,
)


async def create_wallet_service(wallet_create_scheme: WalletCreateScheme) -> WalletScheme:
    async with registry.session() as session:
        wallet = Wallet(user_uid=wallet_create_scheme.user_uid)
        session.add(wallet)
        await session.commit()

    return WalletScheme.from_orm(wallet)


async def get_wallets_by_uuid_service(
        user_uid: UUID | None = None, wallet_uid: UUID | None = None
) -> list[WalletScheme]:
    redis_key = f"wallet_or_user_id_{user_uid or wallet_uid}"
    data = cache_service.get_cache(redis_key)
    if data:
        return [json.loads(d) for d in data]
    async with registry.session() as session:
        if wallet_uid:
            stmt = select(Wallet).where(Wallet.id == wallet_uid)
        elif user_uid:
            stmt = select(Wallet).where(Wallet.user_uid == user_uid)
        else:
            raise ValueError("user_uid or wallet_uid is required")
        result = (await session.execute(stmt)).scalars().all()

        if not result:
            raise HTTPException(status_code=404)
        result = [WalletScheme.from_orm(row) for row in result]
        cache_service.set_cache(redis_key, [WalletScheme.json(row) for row in result])
        return result


async def get_money_service(receiver: TransactionGetMoneyScheme) -> TransactionResponseScheme:
    return await create_transaction_service(
        TransactionCreateScheme(
            id=uuid.uuid4(),
            sender_wallet_id=uuid.UUID("418cb2f3-2fcb-4a57-bbce-4228f33b17c9"),
            receiver_wallet_id=receiver.receiver_wallet_id,
            amount=receiver.amount,
        )
    )


async def run_transaction(_session: AsyncSession, stmt: str) -> None:
    result = await _session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=400, detail="Transaction failed")


async def create_transaction_service(
        transaction_scheme: TransactionCreateScheme,
) -> TransactionResponseScheme:
    async with registry.session() as session:
        stmt = select(Transaction).where(Transaction.id == transaction_scheme.id)
        result = (await session.execute(stmt)).scalars().all()
        if len(result):
            return TransactionResponseScheme(
                id=transaction_scheme.id,
                is_done=False,
                description="Transaction already exists",
            )
        session.begin()
        send_money_stmt = (
            update(Wallet)
            .where(Wallet.id == transaction_scheme.sender_wallet_id)
            .where(Wallet.id != transaction_scheme.receiver_wallet_id)
            .where(Wallet.balance >= transaction_scheme.amount)
            .where(Wallet.is_active)
            .values(balance=Wallet.balance - transaction_scheme.amount)
        )
        receive_money_stmt = (
            update(Wallet)
            .where(Wallet.id == transaction_scheme.receiver_wallet_id)
            .where(Wallet.id != transaction_scheme.sender_wallet_id)
            .where(Wallet.is_active == True)
            .values(balance=Wallet.balance + transaction_scheme.amount)
        )

        # we sort it to avoid deadlock with concurrent queries
        stmt_list = sorted(
            [
                (send_money_stmt, transaction_scheme.sender_wallet_id),
                (receive_money_stmt, transaction_scheme.receiver_wallet_id),
            ],
            key=lambda x: x[1],
        )

        await run_transaction(session, stmt_list[0][0])
        await run_transaction(session, stmt_list[1][0])

        new_transaction = Transaction(
            id=transaction_scheme.id,
            amount=transaction_scheme.amount,
            receiver_id=transaction_scheme.receiver_wallet_id,
            sender_id=transaction_scheme.sender_wallet_id,
            is_done=True,
        )
        kafka_message = jsonable_encoder(
            {
                "wallet_out_id": transaction_scheme.sender_wallet_id,
                "wallet_in_id": transaction_scheme.receiver_wallet_id,
                "amount": transaction_scheme.amount,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        session.add(new_transaction)
        session.add(Event.create(kafka_message))

        await session.flush()
        await session.commit()
        return TransactionResponseScheme(
            id=transaction_scheme.id,
            is_done=new_transaction.is_done,
            description="",
        )
