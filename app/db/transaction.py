import uuid
from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy import DateTime, func
from sqlalchemy.sql.sqltypes import DECIMAL, Boolean, UUID

from .registry import registry

Base = registry.base


class Transaction(Base):  # type: ignore
    __tablename__ = "transaction"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(ForeignKey("wallet.id"), nullable=False, index=True)
    receiver_id = Column(ForeignKey("wallet.id"), nullable=False, index=True)
    amount = Column(DECIMAL(precision=20, scale=2), nullable=False)
    is_done = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)

    __table_args__ = (CheckConstraint("amount >= 0", name="check_balance_positive"),)
