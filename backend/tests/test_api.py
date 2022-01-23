from django.urls import reverse
from phillydb import PhillyCartoTable
import os
import pandas as pd
import pytest
from requests import get as request_get  # so we don't get recursive issues
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
            return [{"rows": [{"mailing_street": "DEF", "mailing_address_1": "IGH"}]}]

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

    request_params = {"startswith_str": "DOMB ALLAN"}
    response = client.get(reverse("autocomplete_list"), request_params)
    assert response.status_code == 200
    assert response.json()["success"] == True


class MockResponse:
    def __init__(self, data=None):
        self.status_code = 200
        self.data = data if data else {}

    def json(self):
        return self.data


@pytest.fixture
def monkeypatch_raw_requests(monkeypatch):
    os.environ["BIOS_URL"] = "https://api.airtable.com"

    def _fake_results(*args, **kwargs):
        if "airtable" in args[0]:
            return MockResponse(
                {
                    "records": [
                        {
                            "fields": {
                                "mailing_street": "ABC Capital",
                                "Notes": "Blah",
                                "name_of_possible_owner": "DEF",
                                "link_to_owner_website": "http://.com",
                            }
                        }
                    ]
                }
            )
        elif "phl.carto" in args[0]:
            return MockResponse(
                {
                    "rows": [
                        {
                            "mailing_street": "ABC Street",
                            "mailing_address_1": "Address1",
                        }
                    ]
                }
            )

    monkeypatch.setattr("requests.get", _fake_results)


@pytest.fixture
def monkeypatch_airtable(monkeypatch):
    os.environ["BIOS_URL"] = "https://api.airtable.com"

    def _fake_results(*args, **kwargs):
        if "airtable" in args[0]:
            return MockResponse(
                {
                    "records": [
                        {
                            "fields": {
                                "mailing_street": "ABC Capital",
                                "Notes": "Blah",
                                "name_of_possible_owner": "DEF",
                                "link_to_owner_website": "http://.com",
                            }
                        }
                    ]
                }
            )
        else:
            return request_get(*args, **kwargs)

    monkeypatch.setattr("requests.get", _fake_results)


def test_mailing_street_bios_response(client, monkeypatch_raw_requests):
    request_params = {"mailing_street": "ABC Capital"}
    response = client.get(reverse("bios_list"), request_params)
    assert response.status_code == 200


def test_property_page_response(client, monkeypatch_airtable):
    request_params = {"parcel_number": "888058983"}
    response = client.get(reverse("property_page_list"), request_params)
    assert response.status_code == 200
