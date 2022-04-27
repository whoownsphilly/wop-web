import numpy as np
import pandas as pd

from backend.queries.queries import (
    carto_request,
)
import asyncio


async def properties_by_parcel_lists_results(**kwargs):
    tasks = []
    for list_name, parcel_numbers in kwargs.items():
        parcel_number_str = ",".join([f"'{num}'" for num in parcel_numbers.split(",")])
        where_str = f"WHERE parcel_number in ({parcel_number_str})"
        dfs = tasks.append(_get_neighborhood_results(where_str, list_name=list_name))
    dfs = await asyncio.gather(*tasks)
    output = {k: v for d in dfs for k, v in d.items()}
    return {"saved_properties": output}


async def properties_by_organizability_results(
    northeast_lat,
    southwest_lat,
    northeast_lng,
    southwest_lng,
    zip_code,
    search_by,
    building_types,
    must_have_rental_license=False,
    n_results=100,
):
    # building_types, add a single quote around each type
    building_type_str = ",".join(
        [f"'{build_type}'" for build_type in building_types.split(",")]
    )
    where_str = f"WHERE category_code_description in ({building_type_str})\n"

    if search_by == "mapBoundary" and southwest_lat != "null":
        where_str += f"""
        AND
            ST_contains(
             ST_MakeEnvelope({southwest_lng},{southwest_lat},{northeast_lng}, {northeast_lat},4326),
             the_geom
          )
        """
    elif search_by == "zipCode" and zip_code != "null":
        where_str += f"AND zip_code = '{zip_code}'"
    return await _get_neighborhood_results(where_str, n_results=n_results)


async def _get_neighborhood_results(
    where_str, list_name="searched_properties", n_results=None
):
    limit_str = f"LIMIT {n_results}" if n_results else ""
    query = f"""
        SELECT ST_Y(opp.the_geom) AS lat, ST_X(opp.the_geom) AS lng, opp.category_code_description, opp.location, opp.unit, rtt.property_count, opp.owner_1, opp.owner_2, opp.mailing_street, opp.mailing_address_1, opp.parcel_number, n_complaints, n_violations, n_violations_open, 
        CASE WHEN has_rental_license is not null THEN True ELSE False END as has_rental_license 
        from opa_properties_public opp
        JOIN (
            SELECT opa_account_num, count(*) as n_violations_open
             from violations
        where violationdate > '2018-01-01' and violationstatus = 'OPEN'
             group by opa_account_num 
         ) v_open
        ON v_open.opa_account_num = opp.parcel_number
        LEFT JOIN (
            SELECT opa_account_num, count(*) as n_complaints 
             from complaints 
        where complaintdate > '2018-01-01'
             group by opa_account_num 
         ) c
        ON c.opa_account_num = opp.parcel_number
        LEFT JOIN (
            SELECT opa_account_num, count(*) as n_violations
             from violations
        where violationdate > '2018-01-01'
             group by opa_account_num 
         ) v
        ON v.opa_account_num = opp.parcel_number
        LEFT JOIN (
            -- This could be done better to get the current property count
            SELECT opa_account_num, max(property_count) as property_count
             from rtt_summary
             GROUP by opa_account_num
         ) rtt
        ON rtt.opa_account_num = opp.parcel_number
        LEFT JOIN (
            SELECT opa_account_num, count(*) as has_rental_license
             from business_licenses
        where licensetype = 'Rental'  and licensestatus = 'Active'
             group by opa_account_num 
         ) l
        ON l.opa_account_num = opp.parcel_number
    {where_str}
    ORDER BY n_violations_open desc
    {limit_str}
    """
    df = (await carto_request(query)).replace({np.nan: None})
    return {list_name: df.to_dict("records")}
