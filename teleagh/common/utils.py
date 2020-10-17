from enum import Enum
from typing import Union, Type, Any
from unittest import mock

from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import resolve
from django.views import View
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.viewsets import GenericViewSet
from typing import List, Tuple


class CustomEnum(Enum):

    def __str__(self) -> str:
        return self.name

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(tag.name, tag.value) for tag in cls]


def setup_view(view: Union[GenericViewSet, View], request, *args, **kwargs):
    """
    Initializes generic view or viewset with passed params
    """
    if isinstance(view, GenericViewSet):
        view.action_map = {}
        view.request = view.initialize_request(request)
    else:
        view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class ResponseFactory:
    ALLOWED_METHODS = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head'}
    VIEWSET_KNOWN_ACTIONS = {'list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'}

    def __init__(self, url, method=None, user=None, data=None, view_kwargs=None, request_factory=APIRequestFactory):
        self.url = url
        self.method = method
        self.user = user
        self.data = data
        self.view_kwargs = view_kwargs or {}
        self.request_factory = request_factory
        self.request = self.get_request()

    def get_request(self) -> HttpRequest:
        request_factory = APIRequestFactory()
        request_method = getattr(request_factory, self.method)
        request = request_method(self.url, data=self.data)
        self._authenticate_request(request)
        return request

    def _authenticate_request(self, request) -> None:
        if self.user:
            force_authenticate(request, self.user)

    def get(self):
        return resolve(self.url).func(self.request, **self.view_kwargs)


def get_mocked_queryset(queryset_class: 'Type[QuerySet[Any]]' = QuerySet):
    m_queryset = mock.Mock(spec=queryset_class)
    m_queryset.filter.return_value = m_queryset
    m_queryset.exclude.return_value = m_queryset
    m_queryset.annotate.return_value = m_queryset
    m_queryset.select_related.return_value = m_queryset
    m_queryset.prefetch_related.return_value = m_queryset
    return m_queryset
