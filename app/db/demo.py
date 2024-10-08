from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import String

from .registry import registry

Base = registry.base


class DemoModel(Base):  # type: ignore
    __tablename__ = "demo_model"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type_ = Column("type", String(256), nullable=False)
