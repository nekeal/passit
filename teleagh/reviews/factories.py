import factory

from .models import Review, SubjectReview, LecturerReview
from ..lecturers.factories import LecturerFactory
from ..subject.factories import SubjectFactory


class ReviewFactory(factory.DjangoModelFactory):
    content = 'review'
    recommended = False

    class Meta:
        model = Review


class SubjectReviewFactory(factory.DjangoModelFactory):
    subject = factory.SubFactory(SubjectFactory)

    class Meta:
        model = SubjectReview


class LecturerReviewFactory(factory.DjangoModelFactory):
    subject = factory.SubFactory(LecturerFactory)

    class Meta:
        model = LecturerReview
