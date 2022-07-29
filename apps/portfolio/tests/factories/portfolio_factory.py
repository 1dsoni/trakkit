from factory import Faker
from factory.django import DjangoModelFactory

from apps.portfolio.models import Portfolio


class PortfolioFactory(DjangoModelFactory):
    name = Faker("name")
    user_id = Faker('uuid4')

    class Meta:
        model = Portfolio
