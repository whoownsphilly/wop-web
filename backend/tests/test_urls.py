from django.urls import resolve, reverse
from django.test import Client
import pytest

from backend.urls import api_urlpatterns


@pytest.fixture
def django_client():
    return Client()


def test_url_resolution(client):
    for urlpattern in api_urlpatterns:
        route = urlpattern.pattern._route
        assert resolve(f"/{route}") is not None


def test_api_settings_url(django_client):
    response = django_client.get(reverse("settings"))
    assert "latest_api_version" in response.json().keys()
