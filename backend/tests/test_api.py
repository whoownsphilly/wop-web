from django.urls import reverse
from phillydb.tables import PhiladelphiaCartoDataTable
import pandas as pd
import pytest

from backend.api import (
    settings_response,
    properties_response,
    permits_response,
    licenses_response,
    violations_response,
    condominiums_response,
    complaints_response,
    appeals_response,
    real_estate_tax_delinquencies_response,
    real_estate_transfers_response,
    case_investigations_response,
)
from backend.urls import table_api_urlpatterns


from rest_framework.test import APIRequestFactory


@pytest.fixture
def request_params():
    return {
        "search_query": "ABC",
        "search_type": "owner",
        "search_method": "contains",
    }


def test_api_responses(client):
    for urlpattern in table_api_urlpatterns:
        route = urlpattern.pattern._route
        assert client.get(f"/{route}") is not None


@pytest.fixture
def monkeypatch_query_by_opa_account_numbers(monkeypatch):
    def _fake_results(*args, **kwargs):
        return pd.DataFrame([{"ABC": "DEF"}])

    monkeypatch.setattr(
        PhiladelphiaCartoDataTable, "query_by_opa_account_numbers", _fake_results
    )


@pytest.fixture
def monkeypatch_query_by_single_str_column(monkeypatch):
    def _fake_results(*args, **kwargs):
        return pd.DataFrame([{kwargs.get("search_column"): "FAKE RESULT"}])

    monkeypatch.setattr(
        PhiladelphiaCartoDataTable, "query_by_single_str_column", _fake_results
    )


def test_property_response(
    client, request_params, monkeypatch_query_by_opa_account_numbers
):
    response = client.get(reverse("properties_list"), request_params)
    assert response.status_code == 200
    assert response.json()["results"] == [{"ABC": "DEF"}]

    request_params["search_method"] = "blah"
    response = client.get(reverse("properties_list"), request_params)
    assert response.status_code != 200


def test_settings_response(client):
    response = client.get(reverse("settings"))
    assert response.status_code == 200


def test_autocomplete_response(client, monkeypatch_query_by_single_str_column):
    request_params = {"startswith_str": "1625 Chest"}
    response = client.get(reverse("autocomplete_list"), request_params)
    assert response.status_code == 200
    assert response.json()["results"] == [{"location": "FAKE RESULT"}]

    request_params = {"startswith_str": "DOMB ALLAN", "column": "owner_1"}
    response = client.get(reverse("autocomplete_list"), request_params)
    assert response.status_code == 200
    assert response.json()["results"] == [{"owner_1": "FAKE RESULT"}]
