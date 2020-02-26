import factory
from factory.fuzzy import FuzzyChoice

from accounts.models import CustomUser, UserProfile, Membership, MembershipTypeChoices
from subject.factories import FieldOfStudyOfAgeGroupFactory


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
    field_age_group = factory.SubFactory(FieldOfStudyOfAgeGroupFactory)
    type = FuzzyChoice(MembershipTypeChoices.choices(), getter=lambda c: c[0])

    class Meta:
        model = Membership
