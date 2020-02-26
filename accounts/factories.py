import factory

from accounts.models import CustomUser, UserProfile, Membership
from subject.models import FieldOfStudyOfAgeGroup


class UserProfileFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('accounts.factories.UserFactory')

    class Meta:
        model = UserProfile


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: f'user {n}')
    email = factory.Faker('email')

    class Meta:
        model = CustomUser


class MembershipFactory(factory.DjangoModelFactory):
    profile = factory.SubFactory(UserProfileFactory)
    field_age_group = factory.SubFactory(FieldOfStudyOfAgeGroup)

    class Meta:
        model = Membership
