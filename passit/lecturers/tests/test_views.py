from unittest import mock

from ...common.utils import setup_view
from ..querysets import LecturerQuerySet
from ..serializers import LecturerBaseSerializer
from ..views import LecturerViewSet


class TestLecturerViewSet:
    def test_correct_serializer_is_used(self, api_rf):
        request = api_rf.get("/api/lecturers/")
        view = setup_view(LecturerViewSet(), request)
        assert view.get_serializer_class() == LecturerBaseSerializer

    def test_correct_queryset_is_used(self, api_rf, monkeypatch):
        request = api_rf.get("/api/lecturers/")
        view = setup_view(LecturerViewSet(), request)
        m_manager = mock.Mock()
        monkeypatch.setattr(LecturerQuerySet, "all", m_manager)

        view.get_queryset()
        m_manager.assert_called_once_with()
