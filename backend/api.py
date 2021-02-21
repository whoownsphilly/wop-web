from django.http import JsonResponse
from phillydb import construct_search_query
from phillydb.tables import (
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


def _table_response(table_obj, request):
    search_query = request.GET.get("search_query", "")
    search_type = request.GET.get("search_type", "")
    search_method = request.GET.get("search_method", "contains")
    try:
        opa_account_numbers_sql = construct_search_query(
            search_query=search_query,
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
            "odb_link": table_obj.get_odb_link(),
            "cartodb_link": table_obj.get_cartodb_link(),
            "search_query": search_query,
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
