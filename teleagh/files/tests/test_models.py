from ..factories import FileFactory
from ..models import File


class TestFileQuerySet:

    def test_filter_by_profile_queryset_method(self, user_profile1, user_profile2):
        expected = FileFactory.create_batch(2, created_by=user_profile1)
        FileFactory.create_batch(2, created_by=user_profile2)
        qs = File.objects.filter_by_profile(user_profile1)
        assert set(expected) == set(qs)
