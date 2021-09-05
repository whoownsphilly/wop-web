from django.http import JsonResponse
from django.core.cache import cache
import base64

import os
import pandas as pd
import numpy as np
from phillydb.exceptions import (
    SearchTypeNotImplementedError,
    SearchMethodNotImplementedError,
)
from phillydb import __version__ as philly_db_version
from phillydb import PhillyCartoQuery
from phillydb.owner_search_queries import OwnerQuery, OwnerQueryResult
from phillydb.utils import get_normalized_address
from phillydb import Properties, construct_search_query

import requests
import simplejson


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

    try:
        search_to_match = get_normalized_address(startswith_str)
    except Exception:
        return PrettifiableJsonResponse(
            {
                "success": True,
                "metadata": {},
                "results": [],
            },
            pretty_print=pretty_print,
        )

    def _get_where_str(search_str):
        search = search_str.split(" ")
        # This more complicated SQL allows for things like
        # 1850 ABC St, 1846 ABC St, and 1840 ABC St
        # to all be captured if a property is labelled internally
        # as 1844-1850 ABC St
        includes_dir = len(search) > 1 and search[1] in ["N", "S", "E", "W"]
        first_word_split = search[0].split("-")
        address_low = int(first_word_split[0])
        address_high = int(first_word_split[1]) if len(first_word_split) > 1 else None
        street_name = (
            search[1]
            if not includes_dir and len(search) > 1
            else (search[2] if len(search) > 2 else "")
        )
        unit = ""
        for i, maybe_unit_str in enumerate(search):
            if "UNIT" in maybe_unit_str and len(search) > i:
                unit = search[i + 1]

        address_floor = address_low - (address_low % 100)
        address_remainder = address_low - address_floor
        address_ceil = address_high + address_floor if address_high else address_low
        unit_str = f"AND UNIT LIKE '%{unit}%'" if unit else ""
        street_dir_str = (
            f"AND STREET_DIRECTION LIKE '%{search[1]}%'" if includes_dir else ""
        )

        pandas_loc_sql_string = "location"
        pandas_loc_sql_string += "||' '||unit" if unit else ""
        return (
            pandas_loc_sql_string,
            f"""
        (
            (
                (
                    cast(HOUSE_NUMBER as int) >= {address_low}
                    AND cast(HOUSE_NUMBER as int) <= {address_ceil}
                )
                OR (
                    cast(HOUSE_NUMBER as int)>= {address_floor}
                    AND cast(HOUSE_NUMBER as int) <= {address_ceil}
                    AND cast(HOUSE_EXTENSION as int) >= {address_remainder}
                )
            )
            AND STREET_NAME LIKE '%{street_name}%'
            {street_dir_str}
            {unit_str}
        )
        """,
        )

    pandas_loc_sql_string, alternate_where_sql = _get_where_str(search_to_match)
    search_to_match_like_str = "%".join(search_to_match.split(" "))
    where_sql = f"""{pandas_loc_sql_string} like '{search_to_match_like_str}%'
        OR ({alternate_where_sql})
        """

    addresses_df = (
        Properties().list(
            columns=[
                "location",
                "unit",
                "parcel_number",
                "owner_1",
                "owner_2",
                "mailing_street",
                "mailing_address_1",
            ],
            where_sql=where_sql,
            limit=n_results,
        )
    ).to_dataframe()

    ### Clean up some of the strings that will be shown on the search bar
    addresses_df["location_unit"] = (
        addresses_df["location"] + " " + addresses_df["unit"].fillna("")
    ).str.strip()

    def _compile_owner_str(x):
        owner_str = x["owner_1"]
        if x.get("owner_2") is not None:
            owner_str += ", " + x["owner_2"]
        return owner_str

    def _compile_if_not_none(x, columns, join_str):
        out_str_list = []
        for col in columns:
            if pd.notnull(x[col]) and len(x[col]) > 0:
                out_str_list.append(x[col])
        return join_str.join(out_str_list)

    addresses_df["owners"] = addresses_df.apply(
        lambda x: _compile_if_not_none(x, ["owner_1", "owner_2"], join_str=", "), axis=1
    )
    addresses_df["full_mailing_address"] = addresses_df.apply(
        lambda x: _compile_if_not_none(
            x, ["mailing_street", "mailing_address_1"], join_str=" "
        ),
        axis=1,
    )
    addresses_df["description"] = addresses_df.apply(
        lambda x: _compile_if_not_none(
            x, ["owners", "full_mailing_address"], join_str="|"
        ),
        axis=1,
    )

    results = addresses_df.to_dict("records")
    return PrettifiableJsonResponse(
        {
            "success": True,
            "metadata": {},
            "results": results,
        },
        pretty_print=pretty_print,
    )


def _table_response(table_obj, request):
    """
    search_to_match: string to use to match
    search_type: what column to use
    search_method: [contains, starts with, ends with, eequals]
    """
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    search_to_match = request.GET.get("search_to_match", "")
    search_type = request.GET.get("search_type", "")
    search_method = request.GET.get("search_method", "contains")
    groupby_col_str = request.GET.get("groupby_cols")
    groupby_cols = groupby_col_str.split(",") if groupby_col_str else []

    data_key = base64.b64encode(
        f"{table_obj.cartodb_table_name}_"
        f"{search_to_match}_{search_type}_"
        f"{search_method}".encode("utf-8")
    )

    data = cache.get(data_key)
    if not data:
        try:
            if search_type == "owner":
                owner_query_obj = OwnerQuery(search_to_match)
                opa_account_numbers_sql = owner_query_obj.parcel_num_sql
            else:
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
            opa_account_numbers=opa_account_numbers_sql, columns="all"
        ).to_dataframe()
        if search_type == "owner":
            owner_query_result_obj = OwnerQueryResult(
                owner_query_obj.parcel_num_sql, owner_query_obj.owners_list
            )
            df = owner_query_result_obj.get_filtered_df(df, table_obj.dt_column)
        value_counts = (
            df.value_counts(groupby_cols)
            .reset_index()
            .rename(columns={0: "count"})
            .to_dict("records")
            if groupby_cols and not df.empty
            else {}
        )

        def _make_col_dict(col):
            # for vue-good-tables format
            column_dict = {"label": col, "field": col, "tooltip": f"Tooltip for {col}"}
            column_dict["filterOptions"] = {"enabled": True}
            if col.endswith("date"):
                column_dict["type"] = "date"
                column_dict["dateInputFormat"] = "yyyy-MM-dd'T'HH':'mm':'ss'Z'"
                column_dict["dateOutputFormat"] = "MMM do yyy"
            return column_dict

        columns = [_make_col_dict(col) for col in df.columns]
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
            "results": {
                "columns": columns,
                "value_counts": value_counts,
                "rows": df.where(pd.notnull(df), None)
                .replace([np.nan], [None])
                .to_dict("records"),
            },
        }
        cache.set(data_key, data)
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
    mailing_address_1 = request.GET.get("mailing_address_1", "")
    output_response = {
        "metadata": {
            "mailing_street": mailing_street,
            "mailing_address_1": mailing_address_1,
        }
    }
    if mailing_street:
        airtable_url = os.environ.get("BIOS_URL")
        # TODO (ssuffian): This should be synced to the db rather than called each time.
        if airtable_url:
            # TODO Change to visible fields to lock it down better
            invisible_fields = ["last_modified_by", "researcher"]
            params = {
                "filterByFormula": 'IF(AND({mailing_street}="'
                + mailing_street
                + '",'
                + '{mailing_address_1}="'
                + mailing_address_1
                + '",'
                + "{show_on_website}=TRUE()),"
                + "TRUE(), FALSE())",
                #'fields': [],
            }
            response = requests.get(airtable_url, params=params)
            if "records" in response.json():
                output_response["results"] = []
                output_response["n_results"] = len(response.json()["records"])
                for record in response.json()["records"]:
                    outputs = {
                        key: val
                        for key, val in record["fields"].items()
                        if key not in invisible_fields
                    }
                    output_response["results"].append(outputs)
                return JsonResponse(output_response)
    output_response["error"] = "Can't find bio."
    return PrettifiableJsonResponse(output_response, pretty_print=pretty_print)


def mailing_address_response(request):
    """Return all properties associated with this mailing address"""
    mailing_street = request.GET["mailing_street"]
    mailing_address_1 = request.GET["mailing_address_1"]
    ## given a mailing address, it returns all properties associated with that address
    ## and plots them?
    where_sql = "mailing_street={mailing_street}"
    addresses_df = (
        Properties().list(
            columns=[
                "location",
                "unit",
                "parcel_number",
                "owner_1",
                "owner_2",
                "mailing_street",
                "mailing_address_1",
            ],
            where_sql=where_sql,
        )
    ).to_dataframe()


def owners_timeline_response(request):
    owner_name = request.GET["owner_name"]
    # optionally add all owners that share that mailing address
    mailing_address = request.GET.get("mailing_address")

    data_key = base64.b64encode(f"{owner_name}_{mailing_address}".encode("utf-8"))
    data = cache.get(data_key)
    if not data:
        owner_query_obj = OwnerQuery(owner_name)

        owner_query_result_obj = OwnerQueryResult(
            owner_query_obj.parcel_num_sql, owner_query_obj.owners_list
        )
        owners_timeline_df = owner_query_result_obj.owners_timeline_df
        owners_timeline_df["location_unit"] = (
            owners_timeline_df["location"] + " " + owners_timeline_df["unit"].fillna("")
        ).str.strip()
        output_response = {
            "success": True,
            "owners_list": owner_query_obj.owner_df.to_dict("records"),
            "owner_timeline": owner_query_result_obj.owners_timeline_df.to_dict(
                "records"
            ),
        }

        data = simplejson.loads(simplejson.dumps(output_response, ignore_nan=True))
        cache.set(data_key, data)
    return JsonResponse(data)
