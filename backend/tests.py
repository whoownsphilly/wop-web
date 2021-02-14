from unittest import TestCase
from django.urls import resolve, reverse
from .urls import urlpatterns
from django.test import Client



class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_resolution(self):
        for urlpattern in urlpatterns:
            route = urlpattern.pattern._route
            assert resolve(f"/{route}") is not None

    def test_api_settings_url(self):
        response = self.client.get(reverse('settings'))
        assert 'latest_api_version' in response.json().keys()
