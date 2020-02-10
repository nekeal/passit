import pytest
from rest_framework.test import APIRequestFactory

pytest_plugins = [
    'news.tests.fixtures',
    'subject.tests.fixtures'
]


@pytest.fixture()
def api_rf():
    return APIRequestFactory()
