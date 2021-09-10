from django.urls import reverse
from phillydb import PhillyCartoTable
import os
import pandas as pd
import pytest
from rest_framework.test import APIRequestFactory

from backend.urls import table_api_urlpatterns, table_schema_api_urlpatterns


@pytest.fixture
def request_params():
    return {
        "search_query": "ABC",
        "search_type": "mailing_address",
        "search_method": "contains",
    }


def test_api_responses(client):
    for urlpattern in table_api_urlpatterns:
        route = urlpattern.pattern._route
        assert client.get(f"/{route}") is not None


class MockPhillyQueryResult:
    def __init__(self, *args, **kwargs):
        pass

    def to_dataframe(self):
        return pd.DataFrame(
            [
                {
                    "location": "DEF",
                    "owner_1": "Joe",
                    "owner_2": "Jill",
                    "parcel_number": "1234",
                }
            ]
        )


def test_schema_api_responses(client, monkeypatch):
    for urlpattern in table_schema_api_urlpatterns:
        route = urlpattern.pattern._route

        def _fake_results(*args, **kwargs):
            return [{"ABC": "DEF"}]

        monkeypatch.setattr(PhillyCartoTable, "get_schema", _fake_results)
        assert client.get(f"/{route}") is not None


@pytest.fixture
def monkeypatch_query_by_opa_account_numbers(monkeypatch):
    def _fake_results(*args, **kwargs):
        return MockPhillyQueryResult()

    monkeypatch.setattr(PhillyCartoTable, "query_by_opa_account_numbers", _fake_results)


@pytest.fixture
def monkeypatch_query_by_single_str_column(monkeypatch):
    def _fake_results(*args, **kwargs):
        return MockPhillyQueryResult()

    monkeypatch.setattr(PhillyCartoTable, "query_by_single_str_column", _fake_results)


def test_property_response(
    client, request_params, monkeypatch_query_by_opa_account_numbers
):
    response = client.get(reverse("properties_list"), request_params)
    assert response.status_code == 200
    assert response.json()["results"]["rows"][0]["location"] == "DEF"

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
    assert response.json()["success"] == True

    request_params = {"startswith_str": "DOMB ALLAN", "column": "owner_1"}
    response = client.get(reverse("autocomplete_list"), request_params)
    assert response.status_code == 200
    assert response.json()["success"] == True


class MockBiosResponse:
    def __init__(self, data=None):
        self.status_code = 200
        self.data = data if data else {}

    def json(self):
        return self.data


@pytest.fixture
def monkeypatch_airtable(monkeypatch):
    def _fake_results(*args, **kwargs):
        return MockBiosResponse(
            {
                "records": [
                    {"fields": {"mailing_street": "ABC Capital", "Notes": "Blah"}}
                ]
            }
        )

    os.environ["BIOS_URL"] = "FAKE_URL"
    monkeypatch.setattr("requests.get", _fake_results)


def test_mailing_street_bios_response(client, monkeypatch_airtable):
    request_params = {"mailing_street": "ABC Capital"}
    response = client.get(reverse("bios_list"), request_params)
    assert response.status_code == 200
