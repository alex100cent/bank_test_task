import factory.fuzzy
import uuid

from app.models import CreateDemoScheme, DemoScheme, WalletCreateScheme, TransactionCreateScheme


class CreateDemoSchemeFactory(factory.Factory):
    type = factory.Faker("pystr", min_chars=10, max_chars=128)

    class Meta:
        model = CreateDemoScheme


class DemoSchemeFactory(factory.Factory):
    uid = factory.LazyFunction(uuid.uuid4)
    type_ = factory.Faker("pystr", min_chars=10, max_chars=128)

    class Meta:
        model = DemoScheme


class CreateWalletSchemeFactory(factory.Factory):
    user_uid = factory.LazyFunction(uuid.uuid4)

    class Meta:
        model = WalletCreateScheme


class TransactionCreateSchemeFactory(factory.Factory):
    id = factory.LazyFunction(uuid.uuid4)
    sender_wallet_id = factory.LazyFunction(uuid.uuid4)
    receiver_wallet_id = factory.LazyFunction(uuid.uuid4)
    amount = factory.Faker("pydecimal", left_digits=10, right_digits=2, positive=True)

    class Meta:
        model = TransactionCreateScheme
