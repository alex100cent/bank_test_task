import factory.fuzzy
import json
import uuid

from app import db
from app.db.registry import registry
from tests.utils import AsyncSQLAlchemyFactory


class DemoModelFactory(AsyncSQLAlchemyFactory):
    uid = factory.LazyFunction(uuid.uuid4)
    type_ = factory.Faker("pystr", min_chars=10, max_chars=128)

    class Meta:
        # pylint: disable=unnecessary-lambda-assignment
        model = db.DemoModel
        async_alchemy_get_or_create = ("uid",)
        async_alchemy_session_factory = lambda: registry.session


class WalletModelFactory(AsyncSQLAlchemyFactory):
    id = factory.LazyFunction(uuid.uuid4)
    user_uid = factory.LazyFunction(uuid.uuid4)
    balance = factory.Faker("pydecimal", left_digits=10, right_digits=2, positive=True)
    is_active = factory.Faker("pybool")
    created_at = factory.Faker("date_time_this_year")

    class Meta:
        model = db.Wallet
        async_alchemy_get_or_create = ("id",)
        async_alchemy_session_factory = lambda: registry.session


class TransactionModelFactory(AsyncSQLAlchemyFactory):
    id = factory.LazyFunction(uuid.uuid4)
    sender_id = factory.LazyFunction(uuid.uuid4)
    receiver_id = factory.LazyFunction(uuid.uuid4)
    amount = factory.Faker("pydecimal", left_digits=10, right_digits=2, positive=True)
    is_done = factory.Faker("pybool")
    created_at = factory.Faker("date_time_this_year")

    class Meta:
        model = db.Transaction
        async_alchemy_get_or_create = ("id",)
        async_alchemy_session_factory = lambda: registry.session


class EventModelFactory(AsyncSQLAlchemyFactory):
    id = factory.LazyFunction(uuid.uuid4)
    topic_name = factory.Faker("pystr", min_chars=10, max_chars=128)
    producer = factory.Faker("pystr", min_chars=10, max_chars=128)
    body = factory.LazyFunction(
        lambda: json.dumps(
            {
                "wallet_out_id": str(factory.LazyFunction(uuid.uuid4)),
                "wallet_id_id": str(factory.LazyFunction(uuid.uuid4)),
                "amount": str(
                    factory.Faker("pydecimal", left_digits=10, right_digits=2, positive=True)
                ),
                "created_at": str(factory.Faker("date_time_this_year")),
            }
        )
    )
    status = factory.Faker("pyint", min_value=0, max_value=1)
    created_at = factory.Faker("date_time_this_year")

    class Meta:
        model = db.Event
        async_alchemy_get_or_create = ("id",)
        async_alchemy_session_factory = lambda: registry.session
