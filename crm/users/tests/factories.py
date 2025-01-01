import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from users.models import Role, User


class UserFactory(DjangoModelFactory):
    email = factory.Faker("email")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = factory.Faker("boolean")
    role = FuzzyChoice([role for (role, _) in Role.choices])

    class Meta:
        model = User
        django_get_or_create = ("email",)


class AdminUserFactory(UserFactory):
    is_staff = True
