from .api import _table_response, _table_schema_response
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


def properties_schema_response(request):
    return _table_schema_response(Properties(), request)


def permits_schema_response(request):
    return _table_schema_response(Permits(), request)


def licenses_schema_response(request):
    return _table_schema_response(Licenses(), request)


def violations_schema_response(request):
    return _table_schema_response(Violations(), request)


def condominiums_schema_response(request):
    return _table_schema_response(Condominiums(), request)


def complaints_schema_response(request):
    return _table_schema_response(Complaints(), request)


def appeals_schema_response(request):
    return _table_schema_response(Appeals(), request)


def real_estate_tax_delinquencies_schema_response(request):
    return _table_schema_response(RealEstateTaxDelinquencies(), request)


def real_estate_transfers_schema_response(request):
    return _table_schema_response(RealEstateTransfers(), request)


def case_investigations_schema_response(request):
    return _table_schema_response(CaseInvestigations(), request)
