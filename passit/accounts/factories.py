import factory

from ..subject.factories import FieldOfStudyOfAgeGroupFactory
from .models import CustomUser, Membership, UserProfile


class UserProfileFactory(factory.DjangoModelFactory):
    user = factory.SubFactory("passit.accounts.factories.UserFactory")

    class Meta:
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user {n}")
    email = factory.Faker("email")

    class Meta:
        model = CustomUser


class MembershipFactory(factory.DjangoModelFactory):
    profile = factory.SubFactory(UserProfileFactory)
    field_age_group = factory.SubFactory(FieldOfStudyOfAgeGroupFactory)

    class Meta:
        model = Membership
