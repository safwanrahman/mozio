import pytest
from rest_framework.test import APIClient

from ..documents import ServiceAreaDocument
from . import UserFactory


@pytest.fixture(autouse=True)
def clear_elasticsearch():
    ServiceAreaDocument._index.delete(ignore=[400, 404])
    ServiceAreaDocument.init()
    yield
    ServiceAreaDocument._index.delete(ignore=[400, 404])
    ServiceAreaDocument.init()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_client(api_client):
    user = UserFactory(is_staff=True)
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def provider_client(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    return api_client