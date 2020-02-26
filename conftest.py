import pytest
from rest_framework.test import APIRequestFactory

pytest_plugins = [
    'accounts.tests.fixtures',
    'news.tests.fixtures',
    'subject.tests.fixtures'
]


@pytest.fixture()
def api_rf():
    return APIRequestFactory()
