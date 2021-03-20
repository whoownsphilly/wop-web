from django.http import JsonResponse
from phillydb import (
    construct_search_query,
    Properties,
    Permits,
    Licenses,
    Violations,
    Condominiums,
    Complaints,
    Appeals,
    RealEstateTaxDelinquencies,
    RealEstateTransfers,
    CaseInvestigations,
)

from phillydb.exceptions import (
    SearchTypeNotImplementedError,
    SearchMethodNotImplementedError,
)

from phillydb import __version__ as philly_db_version


def settings_response(request):
    return JsonResponse(
        {"latest_api_version": "v1", "phillydb_version": philly_db_version.__version__}
    )


def autocomplete_response(request):
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
    return JsonResponse(
        {
            "metadata": {
                "startswith_str": startswith_str,
                "column": column,
                "n_results_limit": n_results,
                "n_results_returned": len(df),
            },
            "results": df.to_dict("records"),
        }
    )


def _table_response(table_obj, request):
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
        return JsonResponse({"error": e.message}, status=400)
    except SearchMethodNotImplementedError as e:
        return JsonResponse({"error": e.message}, status=400)

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
    return JsonResponse(data)


def properties_response(request):
    return _table_response(Properties(), request)


def permits_response(request):
    return _table_response(Permits(), request)


def licenses_response(request):
    return _table_response(Licenses(), request)


def violations_response(request):
    return _table_response(Violations(), request)


def condominiums_response(request):
    return _table_response(Condominiums(), request)


def complaints_response(request):
    return _table_response(Complaints(), request)


def appeals_response(request):
    return _table_response(Appeals(), request)


def real_estate_tax_delinquencies_response(request):
    return _table_response(RealEstateTaxDelinquencies(), request)


def real_estate_transfers_response(request):
    return _table_response(RealEstateTransfers(), request)


def case_investigations_response(request):
    return _table_response(CaseInvestigations(), request)
