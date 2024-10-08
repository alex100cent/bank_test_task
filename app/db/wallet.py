import uuid
from sqlalchemy import Column, CheckConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import DECIMAL, Boolean, DateTime

from .registry import registry

Base = registry.base


class Wallet(Base):  # type: ignore
    __tablename__ = "wallet"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_uid = Column(UUID(as_uuid=True), nullable=False, index=True)
    balance = Column(DECIMAL(precision=20, scale=2), nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)

    __table_args__ = (CheckConstraint("balance >= 0", name="check_balance_positive"),)
