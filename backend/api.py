import base64
from django.http import JsonResponse
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
import os
import numpy as np
import pandas as pd
import requests
import simplejson

from phillydb.exceptions import (
    SearchTypeNotImplementedError,
    SearchMethodNotImplementedError,
)
from phillydb import __version__ as philly_db_version
from phillydb import PhillyCartoQuery
from phillydb.owner_search_queries import OwnerQuery, OwnerQueryResult
from phillydb.utils import get_normalized_address
from phillydb import Properties, construct_search_query

from backend.queries import (
    property_page_results,
    property_latest_owner_detail_results,
    property_details_page_results,
    properties_by_owner_name_results,
    properties_by_mailing_address_results,
    properties_by_autocomplete_results,
    airtable_entries_by_mailing_address_results,
    properties_by_organizability_results,
)


class CustomEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.DataFrame):
            return obj.replace({np.nan: None}).to_dict("records")
        elif isinstance(obj, np.int64):
            return int(obj)
        return super().default(obj)


class PrettifiableJsonResponse(JsonResponse):
    """
    Allows for pretty-printing of the JSON response
    """

    def __init__(self, *args, pretty_print=False, **kwargs):

        json_dumps_params = {"indent": 4} if pretty_print else {}
        super().__init__(
            *args,
            json_dumps_params=json_dumps_params,
            encoder=CustomEncoder,
            **kwargs,
        )


async def _cache_page_response(func, request):
    data_key = str(hash(f"{func.__name__}_{request.GET}"))
    output = cache.get(data_key, {})
    request_params = request.GET.dict()
    pretty_print = request_params.pop("pretty_print", False)
    if output:
        output["cache"] = True
    else:
        output.update(await func(**request_params))
        output["cache"] = False
        cache.set(data_key, output)
    output["data_key"] = data_key
    return PrettifiableJsonResponse(output, pretty_print=pretty_print)


async def settings_response(request):
    """Response to give some generic settings, used for testing"""
    return PrettifiableJsonResponse(
        {"latest_api_version": "v1", "phillydb_version": philly_db_version.__version__}
    )


async def autocomplete_response(request):
    """Used to get the mailing_address related properties and response for the owner page"""
    return await _cache_page_response(properties_by_autocomplete_results, request)


async def owner_page_properties_by_mailing_address_response(request):
    """Used to get the mailing_address related properties and response for the owner page"""
    return await _cache_page_response(properties_by_mailing_address_results, request)


async def owner_page_properties_by_owner_name_response(request):
    """Used to get the owner_name related properties and response for the owner page"""
    return await _cache_page_response(properties_by_owner_name_results, request)


async def property_latest_owner_details_response(request):
    """Used to get the information for the header of the results pages"""
    return await _cache_page_response(property_latest_owner_detail_results, request)


async def property_details_page_response(request):
    """Used to get the information for the Property Basics page"""
    return await _cache_page_response(property_details_page_results, request)


async def property_basics_page_response(request):
    """Used to get the information for the Property Basics page"""
    return await _cache_page_response(property_page_results, request)


async def crowd_sourced_response(request):
    """Airtable (Don't cache this response)"""
    request_params = request.GET.dict()
    pretty_print = request_params.pop("pretty_print", False)
    output = await airtable_entries_by_mailing_address_results(**request_params)
    return PrettifiableJsonResponse(output, pretty_print=pretty_print)


async def neighborhoods_page_response(request):
    """Used to get the information for the Property Basics page"""
    return await _cache_page_response(properties_by_organizability_results, request)
