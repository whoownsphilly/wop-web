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
    license_filter,
    owner_occupied_filter,
    condo_filter,
    building_types,
    rental_building_types,
    n_results=100,
):
    if search_by == "mapBoundary" and southwest_lat != "null":
        where_str = f"""
            ST_contains(
             ST_MakeEnvelope({southwest_lng},{southwest_lat},{northeast_lng}, {northeast_lat},4326),
             the_geom
          )
        """
    elif search_by == "zipCode" and zip_code != "null":
        where_str = f" zip_code = '{zip_code}'"

    def boolify_noneify_str(value, none_value=None):
        if value == "true":
            return True
        elif value == "false":
            return False
        elif value is None or value == "":
            return none_value

    include_license_query = boolify_noneify_str(license_filter, none_value=True)
    include_property_query = not boolify_noneify_str(license_filter, none_value=False)
    is_owner_occupied = boolify_noneify_str(owner_occupied_filter)
    in_a_condo = boolify_noneify_str(condo_filter)

    queries_to_run = []
    if include_property_query and include_license_query:
        n_results = int(int(n_results)/2)
    if include_property_query:
        query = NeighborhoodPropertyQuery(building_types=building_types, has_homestead_exemption=is_owner_occupied, in_a_condo=in_a_condo, where_str=where_str, n_results=n_results).query
        queries_to_run.append(query)
    if include_license_query:
        query = NeighborhoodRentalLicenseQuery(rental_building_types=rental_building_types, is_owner_occupied=is_owner_occupied,  where_str=where_str, n_results=n_results).query
        queries_to_run.append(query)

    dfs = await asyncio.gather(*[carto_request(query) for query in queries_to_run])
    df = pd.concat(dfs).replace({np.nan: None})

    return {"searched_properties": df.to_dict("records")}

class NeighborhoodQuery:
    def __init__(self, n_results, where_str):
        self.n_results = n_results
        self.where_str = where_str
        self.limit_str = f"LIMIT {self.n_results}" if self.n_results else ""

class NeighborhoodPropertyQuery(NeighborhoodQuery):
    def __init__(self, building_types:list[str], has_homestead_exemption:bool|None, in_a_condo:bool|None, where_str:str, n_results:int):
        super().__init__(n_results=n_results, where_str=where_str)
        self.building_type_str = ",".join(
            [f"'{build_type.upper()}'" for build_type in building_types.split(",")]
        )
        if has_homestead_exemption is True:
            self.homestead_exemption_str = "homestead_exemption > 0" 
        elif has_homestead_exemption is False:
            self.homestead_exemption_str = "homestead_exemption = 0"
        elif has_homestead_exemption is None:
            self.homestead_exemption_str = "1=1"

        if in_a_condo is True:
            self.in_a_condo_str = "in_a_condo = 1"
        elif in_a_condo is False:
            self.in_a_condo_str = "in_a_condo = 0"
        elif in_a_condo is None:
            self.in_a_condo_str = "1=1"

    @property
    def query(self):
        return f"""
        SELECT 
            ST_Y(the_geom) AS lat, ST_X(the_geom) AS lng, 
            'no-rental-license' as type,
            location, unit, num_units, category_code_description, num_unique_owners, owner_most_ownership, likely_owner_occupied, other_info, parcel_number, zip_code
            FROM
              (
                select
                  the_geom,
                  max(zip_code) as zip_code,
                  max(parcel_number) as parcel_number,
                  max(location) as location,
                  count(*) as num_units,
                  sum(CASE WHEN homestead_exemption > 0 THEN 1 ELSE 0 END) as likely_owner_occupied,
                  mode() within group (order by category_code_description) as category_code_description,
                  count(DISTINCT owner_1) as num_unique_owners,
                  mode() within group (order by owner_1) as owner_most_ownership,
                  CASE WHEN count(distinct(unit)) > 0 THEN null ELSE max(unit) END as unit,
                  null as other_info,
                  MAX(
                    CASE
                      WHEN building_code_description like '%CONDO %' THEN 1
                      ELSE 0
                    END
                  ) as in_condo
                from
                  opa_properties_public
                where upper(category_code_description) in ({self.building_type_str})
                group by
                  the_geom
              ) col
            where
                {self.in_a_condo_str}
                and {self.homestead_exemption_str}
                and {self.where_str}
            order by
              num_units desc
              {self.limit_str}
        """



class NeighborhoodRentalLicenseQuery(NeighborhoodQuery):
    def __init__(self, rental_building_types:list[str], is_owner_occupied: bool|None, where_str:str, n_results:int):
        super().__init__(n_results=n_results, where_str=where_str)
        self.rental_building_type_str = ",".join(
            [f"'{build_type}'" for build_type in rental_building_types.split(",")]
        )
        if is_owner_occupied is True:
            self.owner_occupied_str = "likely_owner_occupied = 'No'"
        elif is_owner_occupied is False:
            self.owner_occupied_str = "likely_owner_occupied = 'Yes'"
        elif is_owner_occupied is None:
            self.owner_occupied_str = "1=1"

    @property
    def query(self):
        return f"""
            select
              ST_Y(the_geom) AS lat, ST_X(the_geom) AS lng, 
              opa_account_num as parcel_number,
              address as location,
              zip_code,
              'has-rental-license' as type,
              unit_num as unit,
              numberofunits as num_units,
              null as category_code_description,
              1 as num_unique_owners,
              opa_owner as owner_most_ownership,
              concat(
                'rental_category:',
                rentalcategory,
                ', legalname:',
                legalname,
                ', rental_expires_on:',
                expirationdate
              ) as other_info,
              owneroccupied as likely_owner_occupied
            from
              (select left(zip,5) as zip_code, * from business_licenses) bl
            where
              licensestatus = 'Active'
              and licensetype = 'Rental'
              and {self.owner_occupied_str}
              and {self.where_str}
              {self.limit_str}
        """


async def _get_neighborhood_results2(
    where_str, list_name="searched_properties", n_results=None
):
    limit_str = f"LIMIT {n_results}" if n_results else ""
    query = f"""
        SELECT ST_Y(opp.the_geom) AS lat, ST_X(opp.the_geom) AS lng, opp.category_code_description, opp.location, opp.unit, rtt.property_count, opp.owner_1, opp.owner_2, opp.mailing_street, opp.mailing_address_1, opp.parcel_number, n_complaints, n_violations, n_violations_open, 
        CASE WHEN has_rental_license is not null THEN True ELSE False END as has_rental_license 
        from opa_properties_public opp
        LEFT JOIN (
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
            SELECT opa_account_num, 
            CASE WHEN count(*) > 0  THEN True ELSE False END as has_rental_license 
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
