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
from phillydb.additional_links import get_street_view_link

import requests
import simplejson


DEEDS_WHERE_CLAUSE = """
    document_type='DEED' OR
    document_type='DEED SHERIFF' OR
    document_type='DEED OF CONDEMNATION' OR
    document_type='DEED LAND BANK'
"""


def _carto_request(query):
    df_json = requests.get(
        f"""
        https://phl.carto.com/api/v2/sql?q={query}
        """
    ).json()
    if "rows" not in df_json:
        raise ValueError(f"{query}\n\n{df_json}")
    data = df_json["rows"]
    return data


class PrettifiableJsonResponse(JsonResponse):
    def __init__(self, *args, pretty_print=False, **kwargs):
        json_dumps_params = {"indent": 4} if pretty_print else {}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


def settings_response(request):
    return PrettifiableJsonResponse(
        {"latest_api_version": "v1", "phillydb_version": philly_db_version.__version__}
    )


def autocomplete_response(request):
    """
    A response that provides a list of properties based on the start of a string

    Attributes
    ----------
    startswith_str
        The string that the owner or property address must start with
    """
    pretty_print = request.GET.get("pretty", "").upper() == "TRUE"
    startswith_str = request.GET.get("startswith_str", "").upper()
    n_results = request.GET.get("n_results", 10)

    search_by_owner = False
    try:
        search_to_match = get_normalized_address(startswith_str)
    except Exception:
        search_by_owner = True
        search_to_match = startswith_str

    if not search_by_owner:

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

    if search_by_owner or addresses_df.empty:
        search_to_match_like_str = "%".join(search_to_match.split(" "))
        search_to_match_like_str_rev = "%".join(search_to_match.split(" ")[::-1])
        where_sql = f"""
            owner_1 like '{search_to_match_like_str}%' OR
            owner_1 like '{search_to_match_like_str_rev}%' OR
            owner_2 like '{search_to_match_like_str}%' OR
            owner_2 like '{search_to_match_like_str_rev}%'
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

    if addresses_df.empty:
        return PrettifiableJsonResponse(
            {
                "success": True,
                "metadata": {},
                "results": [],
            },
            pretty_print=pretty_print,
        )
    else:

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
            lambda x: _compile_if_not_none(x, ["owner_1", "owner_2"], join_str=", "),
            axis=1,
        )
        addresses_df["full_mailing_address"] = addresses_df.apply(
            lambda x: _compile_if_not_none(
                x, ["mailing_street", "mailing_address_1"], join_str=" "
            ),
            axis=1,
        )
        addresses_df["description"] = addresses_df.apply(
            lambda x: _compile_if_not_none(
                x, ["owners", "full_mailing_address"], join_str=" | "
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

    data_key = base64.b64encode(
        f"owners_timeline_{owner_name}_{mailing_address}".encode("utf-8")
    )
    output = cache.get(data_key, {})
    if output:
        output["cache"] = True
        return JsonResponse(output)

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
        "owner_timeline": owner_query_result_obj.owners_timeline_df.to_dict("records"),
    }

    data = simplejson.loads(simplejson.dumps(output_response, ignore_nan=True))
    cache.set(data_key, data)
    data["cache"] = False
    return PrettifiableJsonResponse(data)


def property_latest_owner_details_response(request):
    """This is used to construct the headline on the website"""
    parcel_number = request.GET["parcel_number"]
    data_key = base64.b64encode(f"{parcel_number}".encode("utf-8"))
    output = cache.get(data_key, {})
    if output:
        return JsonResponse(output)
    # Example of record that doesnt match between opa and rtt_summary: 391085600
    # Example of record with no rtt_summary: 302055100
    query = f"""
        SELECT  grantees, legal_remarks, owner_1, owner_2, 
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        location, unit,
        latest_owners.recording_date as latest_deed_date, 
        opa.recording_date as latest_deed_date_mailing_address,
        mailing_street, mailing_address_1, mailing_zip,
        CASE 
            WHEN owner_2 is null THEN owner_1
            ELSE CONCAT(owner_1,';',owner_2)
        END AS latest_owners_opa,
        CASE 
            WHEN grantees is null AND owner_2 is null THEN owner_1
            WHEN grantees is null THEN CONCAT(owner_1,';',owner_2)
            ELSE CONCAT(grantees,' ',legal_remarks) 
        END AS latest_owners
        FROM (
            SELECT * FROM rtt_summary
            WHERE (
              document_type='DEED' OR
              document_type='DEED SHERIFF' OR
              document_type='DEED OF CONDEMNATION' OR
              document_type='DEED LAND BANK') 
            AND opa_account_num='{parcel_number}' 
            ORDER by recording_date DESC limit 1
        ) latest_owners
        FULL JOIN opa_properties_public opa
        ON latest_owners.opa_account_num = opa.parcel_number
        WHERE opa.parcel_number='{parcel_number}'
    """
    data = _carto_request(query)
    if data:
        result = data[0]
        mailing_address_matches_latest_deed = (
            result["latest_deed_date"] == result["latest_deed_date_mailing_address"]
        )
        mailing_street = result["mailing_street"]
        mailing_street = mailing_street if mailing_street else result["location"]
        mailing_address_1 = (
            result["mailing_address_1"] if result["mailing_address_1"] else ""
        )
        mailing_zip = result["mailing_zip"]
        grantees = result["grantees"]
        location = result["location"]
        unit = result["unit"] if result["unit"] else ""
        address = f"{location} {unit}".strip()
        latitude = result["lat"]
        longitude = result["lng"]
        output = {
            "success": True,
            "owner_is_from_deed": grantees is not None,
            "mailing_address_matches_latest_deed": mailing_address_matches_latest_deed,
            "latest_owner": result["latest_owners"].strip(),
            "full_address": address,
            "latest_mailing_street": mailing_street,
            "latest_mailing_address_1": mailing_address_1,
            "latest_mailing_zip": mailing_zip,
            "street_view_link": f"https://cyclomedia.phila.gov/?address={longitude},{latitude}",
        }
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
                output_response = {}
                output_response["results"] = []
                records = response.json()["records"]
                output_response["n_results"] = len(records)
                # TODO (clean this up so there is only maybe one entry per mailing address?
                for record in records:
                    outputs = {
                        key: val
                        for key, val in record["fields"].items()
                        if key not in invisible_fields
                    }
                    output_response["results"].append(outputs)
                if records:
                    single_record = output_response["results"][0]
                    output["owner_by_mailing_address"] = {
                        "name": single_record["name_of_possible_owner"],
                        "url": single_record["link_to_owner_website"],
                    }
                output["crowd_sourced"] = output_response
    else:
        output = {"success": False}
    cache.set(data_key, output)
    output["cache"] = False
    return PrettifiableJsonResponse(output)


def property_page_response(request):
    """Used to get the information for the Property Basics page"""
    parcel_number = request.GET["parcel_number"]
    five_years_ago = (pd.Timestamp.now() - pd.Timedelta(days=365 * 5)).isoformat()
    date_since = request.GET.get("date_since", five_years_ago)
    data_key = base64.b64encode(
        f"property_page_{parcel_number}{date_since}".encode("utf-8")
    )
    output = cache.get(data_key, {})
    if output:
        output["cache"] = True
        return JsonResponse(output)

    query = f"""
        SELECT opp.parcel_number, year_built, 
        CASE 
            WHEN year_built_estimate = 'Y' THEN true 
            ELSE false END 
        as year_built_is_estimate,
        CASE
            WHEN homestead_exemption > 0 THEN true
            ELSE false END
        as has_homestead_exemption,
        opp.location,
        ST_Y(opp.the_geom) AS lat, ST_X(opp.the_geom) AS lng,
        opp.owner_1, opp.owner_2,
        mailing_street, mailing_address_1,
        building_code_description, category_code_description,
        n_violations, n_violations_open, n_violations_serious,
        has_active_rental_license, expiration_date as rental_license_expiration_date,
        r1.recording_date, r1.grantees, r1.grantors, r1.cash_consideration, r1.property_count as n_properties_on_deed,
        a1.market_value as latest_assessment_market_value, a1.latest_assessment_year
        FROM opa_properties_public opp
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_violations
            FROM violations
            WHERE opa_account_num = '{parcel_number}'
            AND violationdate < '{date_since}'

        ) v1
        ON v1.parcel_number = opp.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_violations_open
            FROM violations
            WHERE opa_account_num = '{parcel_number}'
            AND violationstatus = 'OPEN'

        ) v2
        ON v1.parcel_number = v2.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_violations_serious
            FROM violations
            WHERE opa_account_num = '{parcel_number}'
            AND caseprioritydesc in ('HAZARDOUS', 'UNSAFE', 'IMMINENTLY DANGEROUS')
            AND violationdate < '{date_since}'
        ) v3
        ON v1.parcel_number = v3.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number,
            CASE WHEN count(*) > 0 THEN TRUE ELSE FALSE END as has_active_rental_license,
            max(expirationdate) as expiration_date
            FROM business_licenses
            WHERE opa_account_num = '{parcel_number}'
            AND licensetype='Rental'
            AND licensestatus='Active'
        ) l1
        ON v1.parcel_number = l1.parcel_number
        LEFT JOIN (
            SELECT opa_account_num as parcel_number,
            *
            FROM rtt_summary
            WHERE opa_account_num = '{parcel_number}'
            AND (
                {DEEDS_WHERE_CLAUSE}
            )
            ORDER BY recording_date desc LIMIT 1
        ) r1
        ON v1.parcel_number = r1.parcel_number
        LEFT JOIN (
            SELECT parcel_number,
            year as latest_assessment_year,
            market_value
            FROM assessments a
            WHERE parcel_number = '{parcel_number}'
            ORDER BY year DESC LIMIT 1
        ) a1
        ON v1.parcel_number = a1.parcel_number
        WHERE opp.parcel_number = '{parcel_number}'
        """

    data = _carto_request(query)

    if len(data) > 0:
        output.update(data[0])
        mailing_street = output["mailing_street"]
        mailing_address_1 = output["mailing_address_1"]
        airtable_url = os.environ.get("BIOS_URL")
        if airtable_url and mailing_street and mailing_address_1:
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
                "fields": ["name_of_possible_owner", "link_to_owner_website"],
            }
            response = requests.get(airtable_url, params=params).json()
            if "records" in response:
                airtable_result = response["records"][0]["fields"]
                output.update(
                    {
                        "managed_by": airtable_result["name_of_possible_owner"],
                        "link_to_management_website": airtable_result.get(
                            "link_to_owner_website"
                        ),
                    }
                )

    # PROPERTY TIMELINE AND VALUE LIST
    query = f"""
    SELECT * FROM (
        SELECT 
        'purchased' as status, 
        opa_account_num as parcel_number,
        grantees as owner, 
        grantors as seller,
        cash_consideration as property_value, 
        recording_date as date
        FROM rtt_summary
        WHERE opa_account_num = '{parcel_number}'
        AND ({DEEDS_WHERE_CLAUSE})
        UNION ALL
        SELECT
        'assessed' as status, 
        null as owner,
        null as seller,
        parcel_number,
        market_value as property_value,
        CAST(CONCAT(year,'-01-01') as TIMESTAMP) as date  
        FROM assessments
        WHERE parcel_number = '{parcel_number}'
    ) timeline 
    ORDER BY DATE ASC
    """
    assessment_timeline_data = _carto_request(query)
    owner_data_df = pd.DataFrame(
        [deed for deed in assessment_timeline_data if deed["status"] == "purchased"]
    )

    # we aren't going to try to guess ownership before 2000 since that's as far back as the DEEDS table goes (technically it goes back to Dec 6 1999)
    owner_data = []
    earliest_start_time = pd.to_datetime("2000-01-01")
    if len(owner_data_df) > 0:
        first_row_owner = pd.DataFrame(
            [
                {
                    "start": earliest_start_time,
                    "end": owner_data_df.iloc[0]["date"],
                    "owner": owner_data_df.iloc[0]["seller"],
                }
            ]
        )
        owner_data_df["start"] = owner_data_df["date"]
        owner_data_df["end"] = owner_data_df["date"].shift(-1)
        owner_data_df["end"].iloc[-1] = pd.Timestamp.now().isoformat()
        owner_data = pd.concat(
            [first_row_owner, owner_data_df[["start", "end", "owner"]]]
        ).to_dict("records")
    else:
        owners = [output["owner_1"]]
        if output["owner_2"]:
            owners.append(output["owner_2"])
        owner_data = [
            {
                "start": earliest_start_time,
                "owner": ";".join(owners),
                "end": pd.Timestamp.now().isoformat(),
            }
        ]

    output["property_ownership_timeline"] = owner_data
    output["property_value_timeline"] = assessment_timeline_data
    cache.set(data_key, output)
    output["cache"] = False
    return JsonResponse(output)


def owner_current_properties_map_response(request):
    parcel_number = request.GET["parcel_number"]
    data_key = base64.b64encode(
        f"owner_current_properties_map_response_{parcel_number}".encode("utf-8")
    )
    output = cache.get(data_key, {})
    if output:
        return JsonResponse(output)

    query = f"""
        --This Property
        SELECT parcel_number, 
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        opa.market_value,
        location, unit, '' as owners, 'self' as relation, opa.mailing_street, opa.mailing_address_1 
        FROM opa_properties_public opa
        WHERE opa.parcel_number = '{parcel_number}'
        UNION ALL
        -- Owner-Based
        SELECT parcel_number, 
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        opa.market_value,
        location, unit, grantees as owners, 'owner' as relation, opa.mailing_street, opa.mailing_address_1 
        FROM opa_properties_public opa
        INNER JOIN (
          SELECT 
          rtt_summary.opa_account_num, 
          rtt_summary.grantees, 
          rtt_summary.recording_date, 
          document_type, street_address
          FROM rtt_summary
          INNER JOIN 
          (
            SELECT opa_account_num, max(recording_date) as recording_date
            FROM rtt_summary  
            WHERE ({ DEEDS_WHERE_CLAUSE })
            AND grantees in (
               SELECT grantees FROM rtt_summary WHERE (
                  document_type='DEED' OR
                  document_type='DEED SHERIFF' OR
                  document_type='DEED OF CONDEMNATION' OR
                  document_type='DEED LAND BANK'
                ) AND opa_account_num='{parcel_number}' 
                ORDER by recording_date DESC limit 1
            )
            GROUP BY opa_account_num 
          ) grouped_parcels
          ON rtt_summary.recording_date = grouped_parcels.recording_date
          and rtt_summary.opa_account_num = grouped_parcels.opa_account_num
        ) rtt_summary
        ON opa.parcel_number = rtt_summary.opa_account_num
        UNION ALL
        -- Mailing Address
        SELECT parcel_number, 
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        opa.market_value,
        location, unit, concat(opa.owner_1,';',opa.owner_2) as owners, 'mailing_address' as relation, opa.mailing_street, opa.mailing_address_1 
        FROM opa_properties_public opa INNER JOIN (
            SELECT distinct mailing_street, mailing_address_1, mailing_address_2, mailing_zip
            FROM opa_properties_public opa
            WHERE opa.parcel_number = '{parcel_number}' 
            and mailing_street is not null
        ) opa_mailing_address
        ON opa.mailing_street = opa_mailing_address.mailing_street
        AND (opa.mailing_address_1 = opa_mailing_address.mailing_address_1 or opa_mailing_address.mailing_address_1 is null)
        AND (opa.mailing_address_2 = opa_mailing_address.mailing_address_2 or opa_mailing_address.mailing_address_2 is null)
        AND (opa.mailing_zip = opa_mailing_address.mailing_zip or opa_mailing_address.mailing_zip is null)
    """
    owner_property_current_df = pd.DataFrame(_carto_request(query))
    owner_property_current_df["location_unit"] = (
        owner_property_current_df["location"]
        + " "
        + owner_property_current_df["unit"].fillna("")
    ).str.strip()
    # Do a little bit of reformatting to remove properties that were returned
    # both through an owner and mailing address connection
    current_property = owner_property_current_df[
        owner_property_current_df["relation"] == "self"
    ]
    unique_properties = current_property
    owner_based_properties = owner_property_current_df[
        (owner_property_current_df["relation"] == "owner")
        & (
            ~owner_property_current_df.parcel_number.isin(
                unique_properties.parcel_number
            )
        )
    ]
    unique_properties = pd.concat([unique_properties, owner_based_properties])
    mailing_address_based_properties = owner_property_current_df[
        (owner_property_current_df["relation"] == "mailing_address")
        & (
            ~owner_property_current_df.parcel_number.isin(
                unique_properties.parcel_number
            )
        )
    ]
    unique_properties = pd.concat([unique_properties, mailing_address_based_properties])
    output = {
        "success": True,
        "total_value_of_properties": unique_properties["market_value"]
        .sum()
        .astype(float),
        "n_properties": len(unique_properties),
        "owners_currently_owned_properties": unique_properties.to_dict("records"),
    }
    cache.set(data_key, output)
    output["cache"] = False
    return JsonResponse(output)


def owner_page_response(request):
    """
    We need:
    owner timeline (when they owned what)
    ideally a value of their portfolio over time
    same violations, complaints in last N years info
    maybe something about average violations of a property for comparison
    """
    owner_name = request.GET["owner_name"]
    data_key = base64.b64encode(f"owner_page_{owner_name}".encode("utf-8"))
    output = cache.get(data_key, {})
    if output:
        output["cache"] = True
        return JsonResponse(output)
    owner_query_obj = OwnerQuery(owner_name)

    owner_query_result_obj = OwnerQueryResult(
        owner_query_obj.parcel_num_sql, owner_query_obj.owners_list
    )
    owner_property_timeline_df = owner_query_result_obj.owners_timeline_df
    owner_property_timeline_df["location_unit"] = (
        owner_property_timeline_df["location"]
        + " "
        + owner_property_timeline_df["unit"].fillna("")
    ).str.strip()
    owner_property_timeline_df["end_dt"] = owner_property_timeline_df["end_dt"].replace(
        {np.nan: None}
    )
    owner_property_timeline_df["current_owner"] = pd.isnull(
        owner_property_timeline_df["end_dt"]
    )

    # OWNER PROPERTY COUNTS BY NAME
    ##################################################################
    # Get property counts by name for apex grouped bar chart in format:
    # x: {'name': 'currently owned', 'data': [1,2]}
    # y: [ownername1, ownername2, ownername3]
    owner_property_counts_by_name = (
        owner_property_timeline_df.groupby(["likely_owner", "current_owner"])
        .size()
        .to_frame("n_properties")
        .reset_index()
    )
    currently_owned = owner_property_counts_by_name.query(
        "current_owner==True"
    ).set_index("likely_owner")["n_properties"]
    previously_owned = owner_property_counts_by_name.query(
        "current_owner==False"
    ).set_index("likely_owner")["n_properties"]
    # make sure there is an entry for each owner
    all_owned = pd.concat([currently_owned, previously_owned], axis=1).replace(
        {np.nan: None}
    )
    all_owned.columns = ["Currently Owned", "Previously Owned"]
    all_owned.sort_values("Currently Owned", inplace=True, ascending=False)
    chart_data = [
        {"name": key, "data": val} for key, val in all_owned.to_dict("list").items()
    ]
    chart_categories = all_owned.index.tolist()
    ##################################################################

    ## violations

    output = {
        "owner_property_timeline": owner_property_timeline_df.to_dict("records"),
        "owner_property_counts_by_name": {
            "categories": chart_categories,
            "data": chart_data,
        },
    }
    cache.set(data_key, output)
    output["cache"] = False
    return PrettifiableJsonResponse(output)


def bios_response(request):
    """Airtable"""
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


# Allows for responding with data based on a sub-query of parcel numbers
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
