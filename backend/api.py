from django.http import JsonResponse
import os
import pandas as pd
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

    results = {}
    n_results_returned = 0

    is_valid_address = True
    try:
        search_to_match = get_normalized_address(startswith_str)
    except:
        is_valid_address = False
        search_to_match = startswith_str

    def _add_formatted_results(
        results, results_df, name, description_col="parcel_number", url_override=None
    ):
        results_df["url"] = url_override if url_override else name
        cols = [name, "url"]
        col_names = {name: "title"}
        if description_col:
            cols += [description_col]
            col_names[description_col] = "description"
        result_records = results_df[cols].rename(columns=col_names).to_dict("records")
        results[name] = {"name": name, "results": result_records}
        return results

    if is_valid_address:

        def _get_where_str(search_str):
            search = search_str.split(" ")
            # This more complicated SQL allows for things like
            # 1850 ABC St, 1846 ABC St, and 1840 ABC St
            # to all be captured if a property is labelled internally
            # as 1844-1850 ABC St
            includes_dir = len(search) > 1 and search[1] in ["N", "S", "E", "W"]
            first_word_split = search[0].split("-")
            address_low = int(first_word_split[0])
            address_high = (
                int(first_word_split[1]) if len(first_word_split) > 1 else None
            )
            street_name = (
                search[1]
                if not includes_dir and len(search) > 1
                else (search[2] if len(search) > 2 else "")
            )
            address_floor = address_low - (address_low % 100)
            address_remainder = address_low - address_floor
            address_ceil = address_high + address_floor if address_high else address_low

            return f"""
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
            )
            """

        alternate_where_sql = _get_where_str(search_to_match)
        search_to_match_like_str = "%".join(search_to_match.split(" "))
        where_sql = f"""location like '{search_to_match_like_str}%'
            OR ({alternate_where_sql})
            """

        addresses_df = (
            Properties().list(
                columns=["location", "parcel_number", "owner_1", "owner_2"],
                where_sql=where_sql,
                limit=n_results,
            )
        ).to_dataframe()

        results = _add_formatted_results(results, addresses_df, "location")
        results = _add_formatted_results(
            results, addresses_df, "owner_1", url_override="owner"
        )
        results = _add_formatted_results(
            results, addresses_df, "owner_2", url_override="owner"
        )

        n_results_returned += len(addresses_df)

    else:

        search_to_match_like_str = "%".join(search_to_match.split(" "))

        search_to_match_like_str_rev = "%".join(search_to_match.split(" ")[::-1])
        owners_df = (
            PhillyCartoQuery(
                f"""
        SELECT distinct(owner) from (
            SELECT distinct(owner_1) as owner
            FROM opa_properties_public
            WHERE (
                owner_1 like '{search_to_match_like_str}%' OR
                owner_1 like '{search_to_match_like_str_rev}%'
            )
            UNION ALL
            SELECT distinct(owner_2) as owner
            FROM opa_properties_public
            WHERE (
                owner_2 like '{search_to_match_like_str}%' OR
                owner_2 like '{search_to_match_like_str_rev}%'
            )
        ) as owners
        """
            )
            .execute()
            .to_dataframe()
        )
        results = _add_formatted_results(results, owners_df, "owner", "owner")

    return PrettifiableJsonResponse(
        {
            "success": True,
            "metadata": {
                "startswith_str": startswith_str,
                "search_to_match": search_to_match,
                "column": column,
                "n_results_limit": n_results,
                "n_results_returned": n_results_returned,
                "is_valid_address": is_valid_address,
            },
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
        opa_account_numbers=opa_account_numbers_sql
    ).to_dataframe()

    if search_type == "owner":
        owner_query_result_obj = OwnerQueryResult(
            owner_query_obj.parcel_num_sql, owner_query_obj.owners_list
        )
        df = owner_query_result_obj.get_filtered_df(df, table_obj.dt_column)

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
            "rows": df.where(pd.notnull(df), None).to_dict("records"),
        },
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
            # TODO Change to visible fields to lock it down better
            invisible_fields = ["last_modified_by", "researcher"]
            params = {
                "filterByFormula": 'IF({mailing_street}="'
                + mailing_street
                + '",TRUE(), FALSE())',
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
    return PrettifiableJsonResponse(
        output_response, status=404, pretty_print=pretty_print
    )


def owners_timeline_response(request):
    owner_name = request.GET.get("owner_name")
    owner_query_obj = OwnerQuery(owner_name)

    owner_query_result_obj = OwnerQueryResult(
        owner_query_obj.parcel_num_sql, owner_query_obj.owners_list
    )
    owners_timeline_df = owner_query_result_obj.owners_timeline_df
    output_response = {
        "owners_list": owner_query_obj.owner_df.to_dict("records"),
        "owner_timeline": owner_query_result_obj.owners_timeline_df.to_dict("records"),
    }

    return JsonResponse(
        simplejson.loads(simplejson.dumps(output_response, ignore_nan=True))
    )
