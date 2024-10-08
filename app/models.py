from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from uuid import UUID


class DemoScheme(BaseModel):
    uid: UUID
    type_: str = Field(..., alias="type")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CreateDemoScheme(BaseModel):
    type_: str = Field(..., alias="type")


class WalletCreateScheme(BaseModel):
    user_uid: UUID


class WalletScheme(BaseModel):
    id: UUID
    user_uid: UUID
    balance: Decimal
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TransactionScheme(BaseModel):
    id: UUID
    sender_uid: UUID
    receiver_uid: UUID
    amount: Decimal = Field(max_digits=20, decimal_places=2)
    is_done: bool
    created_at: datetime


class TransactionGetMoneyScheme(BaseModel):
    receiver_wallet_id: UUID
    amount: Decimal = Field(max_digits=20, decimal_places=2)


class TransactionCreateScheme(BaseModel):
    id: UUID
    sender_wallet_id: UUID
    receiver_wallet_id: UUID
    amount: Decimal = Field(max_digits=20, decimal_places=2)


class TransactionResponseScheme(BaseModel):
    id: UUID
    is_done: bool
    description: str


class TransactionCreatedOutboxScheme(BaseModel):
    wallet_out_id: UUID
    wallet_id_id: UUID
    amount: Decimal = Field(max_digits=20, decimal_places=2)
    created_at: datetime
