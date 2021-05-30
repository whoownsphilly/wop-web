from django.http import JsonResponse
import os
from phillydb.exceptions import (
    SearchTypeNotImplementedError,
    SearchMethodNotImplementedError,
)
from phillydb import __version__ as philly_db_version
from phillydb import Properties, construct_search_query
import requests


class PrettifiableJsonResponse(JsonResponse):
    def __init__(self, *args, pretty_print=False, **kwargs):
        json_dumps_params = {"indent": 4} if pretty_print else {}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


def settings_response(request):
    return PrettifiableJsonResponse(
        {"latest_api_version": "v1", "phillydb_version": philly_db_version.__version__}
    )


def autocomplete_response(request):
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    startswith_str = request.GET.get("startswith_str", "").upper()
    column = request.GET.get("column", "location")
    n_results = request.GET.get("n_results", 10)
    df = Properties().query_by_single_str_column(
        search_column=column,
        search_to_match=startswith_str,
        search_method="starts with",
        result_columns=["location", "parcel_number"],
        limit=n_results,
    )
    return PrettifiableJsonResponse(
        {
            "metadata": {
                "startswith_str": startswith_str,
                "column": column,
                "n_results_limit": n_results,
                "n_results_returned": len(df),
            },
            "results": df.to_dict("records"),
        },
        pretty_print=pretty_print,
    )


def _table_response(table_obj, request):
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    search_to_match = request.GET.get("search_to_match", "")
    search_query = request.GET.get("search_query", "")
    search_to_match = search_to_match if search_to_match else search_query

    search_type = request.GET.get("search_type", "")
    search_method = request.GET.get("search_method", "contains")
    try:
        opa_account_numbers_sql = construct_search_query(
            search_to_match=search_to_match,
            search_type=search_type,
            search_method=search_method,
        )
    except SearchTypeNotImplementedError as e:
        return PrettifiableJsonResponse(
            {"error": e.message}, status=400, pretty_print=pretty_print
        )
    except SearchMethodNotImplementedError as e:
        return PrettifiableJsonResponse(
            {"error": e.message}, status=400, pretty_print=pretty_print
        )

    df = table_obj.query_by_opa_account_numbers(
        opa_account_numbers=opa_account_numbers_sql
    )

    data = {
        "metadata": {
            "title": table_obj.title,
            "cartodb_table_name": table_obj.cartodb_table_name,
            "data_links": table_obj.data_links,
            "search_query": search_to_match,
            "search_to_match": search_to_match,
            "search_type": search_type,
            "search_method": search_method,
        },
        "results": df.to_dict("records"),
    }
    return PrettifiableJsonResponse(data, pretty_print=pretty_print)


def _table_schema_response(table_obj, request):
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    schema = table_obj.get_schema()
    schema = schema if schema else []
    data = {"metadata": {"url": table_obj._get_schema_link()}, "results": schema}
    return PrettifiableJsonResponse(data, pretty_print=pretty_print)


def bios_response(request):
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    # currently only available for mailing street, but this may be extended some day.
    mailing_street = request.GET.get("mailing_street", "")
    output_response = {"metadata": {"mailing_street": mailing_street}}
    if mailing_street:
        airtable_url = os.environ.get("BIOS_URL")
        # TODO (ssuffian): This should be synced to the db rather than called each time.
        if airtable_url:
            response = requests.get(airtable_url)
            for r in response.json()["records"]:
                if (
                    r["fields"].get("mailing_street")
                    and r["fields"]["mailing_street"] == mailing_street
                ):
                    output_response["results"] = r["fields"]
                    return PrettifiableJsonResponse(
                        output_response, pretty_print=pretty_print
                    )
    output_response["error"] = "Can't find bio."
    return PrettifiableJsonResponse(
        output_response, pretty_print=pretty_print, status=404
    )
