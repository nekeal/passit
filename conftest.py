import pytest
from rest_framework.test import APIRequestFactory

pytest_plugins = [
    'teleagh.accounts.tests.fixtures',
    'teleagh.news.tests.fixtures',
    'teleagh.subject.tests.fixtures',
    'teleagh.events.tests.fixtures',
    'teleagh.files.tests.fixtures'
]


@pytest.fixture()
def api_rf():
    return APIRequestFactory()
