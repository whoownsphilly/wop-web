import numpy as np

from backend.queries.queries import (
    carto_request,
)


async def properties_by_organizability_results(
    northeast_lat,
    southwest_lat,
    northeast_lng,
    southwest_lng,
    zip_code,
    search_by,
    must_have_rental_license=False,
    n_results=100,
):
    where_str = ""
    if search_by == "mapBoundary" and southwest_lat != "null":
        where_str = f"""
        WHERE
            ST_contains(
             ST_MakeEnvelope({southwest_lng},{southwest_lat},{northeast_lng}, {northeast_lat},4326),
             the_geom
          )
        """
    elif search_by == "zipCode" and zip_code != "null":
        where_str = f"WHERE zip_code = '{zip_code}'"
    query = f"""
        SELECT ST_Y(opp.the_geom) AS lat, ST_X(opp.the_geom) AS lng, opp.location, opp.unit, opp.parcel_number, n_complaints, n_violations, has_rental_license from opa_properties_public opp
        JOIN (
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
            SELECT opa_account_num, count(*) as has_rental_license
             from business_licenses
        where licensetype = 'Rental'  and licensestatus = 'Active'
             group by opa_account_num 
            
         ) l
        ON l.opa_account_num = opp.parcel_number
    {where_str}
    ORDER BY n_complaints desc
    LIMIT {n_results}
    """
    df = (await carto_request(query)).replace({np.nan: None})
    return {"properties": df.to_dict("records")}
