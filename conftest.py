import pytest
from rest_framework.test import APIRequestFactory

pytest_plugins = [
    'passit.accounts.tests.fixtures',
    'passit.news.tests.fixtures',
    'passit.subject.tests.fixtures',
    'passit.events.tests.fixtures',
]


@pytest.fixture
def api_rf():
    return APIRequestFactory()
