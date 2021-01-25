from unittest import TestCase
from django.urls import resolve
from .urls import urlpatterns


class TestUrls(TestCase):
    def test_url_resolution(self):
        for urlpattern in urlpatterns:
            route = urlpattern.pattern._route
            assert resolve(f'/{route}') is not None
