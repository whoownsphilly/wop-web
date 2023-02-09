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
        where_str = f"parcel_number in ({parcel_number_str})"

        async def return_results_in_dict(where_str, list_name):
            df = await get_results(where_str_override=where_str)
            return {list_name: df.to_dict("records")}

        dfs = tasks.append(return_results_in_dict(where_str, list_name))
    dfs = await asyncio.gather(*tasks)
    output = {k: v for d in dfs for k, v in d.items()}
    return {"saved_properties": output}


async def properties_by_organizability_results(
    *args,
    starting_latitude,
    starting_longitude,
    num_units_per_list,
    num_lists,
    **kwargs,
):
    num_lists = int(num_lists)
    num_units_per_list = int(num_units_per_list)
    df_orig = await get_results(
        *args,
        num_total_units=num_units_per_list * num_lists,
        starting_latitude=starting_latitude,
        starting_longitude=starting_longitude,
        **kwargs,
    )
    if (
        starting_latitude
        and starting_longitude
        and starting_latitude != "null"
        and starting_longitude != "null"
    ):
        starting_latitude = starting_latitude
        starting_longitude = starting_longitude
    else:
        starting_latitude = df.iloc[0]["lat"]
        starting_longitude = df.iloc[0]["lng"]
    # remove duplicates by sorting by first rental license and removing duplicate by lat/lng
    df_orig = df_orig.sort_values("type").drop_duplicates(["lat", "lng"])

    df_orig = get_walk_list_order(
        df_orig, starting_lat=starting_latitude, starting_lng=starting_longitude
    )
    # Cluster

    # Split
    dfs = np.array_split(df_orig, num_lists)
    results = {}
    for df in dfs:
        name = df.location.iloc[0]
        results[name] = df.to_dict("records")

    return {"searched_properties": df_orig.to_dict("records"), "walk_lists": results}


async def get_results(
    northeast_lat=None,
    southwest_lat=None,
    northeast_lng=None,
    southwest_lng=None,
    zip_code=None,
    address_distance=None,
    starting_latitude=None,
    starting_longitude=None,
    search_by=None,
    license_filter=None,
    owner_occupied_filter=None,
    condo_filter=None,
    building_types=[],
    rental_building_types=[],
    num_total_units=None,
    where_str_override=None,
    list_name="searched_properties",
):
    def boolify_noneify_str(value, none_value=None):
        if value == "true":
            return True
        elif value == "false":
            return False
        elif value is None or value == "" or value == "null":
            return none_value

    def noneify_null_str(value):
        return None if value is None or value == "" or value == "null" else value

    starting_latitude = noneify_null_str(starting_latitude)
    starting_longitude = noneify_null_str(starting_longitude)
    address_distance = noneify_null_str(address_distance)
    zip_code = noneify_null_str(zip_code)
    southwest_lat = noneify_null_str(southwest_lat)
    northeast_lat = noneify_null_str(northeast_lat)
    southwest_lng = noneify_null_str(southwest_lng)
    northeast_lng = noneify_null_str(northeast_lng)
    include_license_query = boolify_noneify_str(license_filter, none_value=True)
    include_property_query = not boolify_noneify_str(license_filter, none_value=False)
    is_owner_occupied = boolify_noneify_str(owner_occupied_filter)
    in_a_condo = boolify_noneify_str(condo_filter)
    if where_str_override:
        where_str = where_str_override
    elif search_by == "mapBoundary" and southwest_lat:
        where_str = f"""
            ST_contains(
             ST_MakeEnvelope({southwest_lng},{southwest_lat},{northeast_lng}, {northeast_lat},4326),
             the_geom
          )
        """
    elif search_by == "zipCode":
        where_str = f" zip_code = '{zip_code}'"
    elif search_by == "address" and address_distance:
        # 1 city block is ~80? meters
        where_str = f"""
            ST_DWithin(
                    the_geom,
              CDB_LatLng({starting_latitude}, {starting_longitude})::geography,
              80 * {address_distance}
            )
        """

    if starting_latitude and starting_longitude:
        order_by_str = f"ST_Distance( the_geom, CDB_LatLng({starting_latitude}, {starting_longitude}))"
    else:
        order_by_str = f"num_units"

    queries_to_run = []
    if include_property_query:
        query = NeighborhoodPropertyQuery(
            building_types=building_types,
            has_homestead_exemption=is_owner_occupied,
            in_a_condo=in_a_condo,
            where_str=where_str,
            n_results=num_total_units,
            order_by_str=order_by_str,
        ).query
        queries_to_run.append(query)
    if include_license_query:
        query = NeighborhoodRentalLicenseQuery(
            rental_building_types=rental_building_types,
            is_owner_occupied=is_owner_occupied,
            where_str=where_str,
            n_results=num_total_units,
            order_by_str=order_by_str,
        ).query
        queries_to_run.append(query)

    dfs = await asyncio.gather(*[carto_request(query) for query in queries_to_run])
    df = pd.concat(dfs).replace({np.nan: None})

    # df = df[df["num_units"].cumsum() <= float(num_total_units)]
    return df


class NeighborhoodQuery:
    def __init__(self, n_results, where_str, order_by_str):
        self.n_results = n_results
        self.where_str = where_str
        self.order_by_str = order_by_str
        self.limit_str = f"LIMIT {self.n_results}" if self.n_results else ""


class NeighborhoodPropertyQuery(NeighborhoodQuery):
    def __init__(
        self,
        building_types: list[str],
        has_homestead_exemption: bool,
        in_a_condo: bool,
        where_str: str,
        order_by_str: str,
        n_results: int,
    ):
        super().__init__(
            n_results=n_results, where_str=where_str, order_by_str=order_by_str
        )
        if building_types:
            building_type_list_str = ",".join(
                [f"'{build_type.upper()}'" for build_type in building_types.split(",")]
            )
            self.building_type_str = (
                f"upper(category_code_description) in ({building_type_list_str})"
            )
        else:
            self.building_type_str = "1=1"
        if has_homestead_exemption is True:
            self.homestead_exemption_str = "likely_owner_occupied > 0"
        elif has_homestead_exemption is False:
            self.homestead_exemption_str = "likely_owner_occupied = 0"
        elif has_homestead_exemption is None:
            self.homestead_exemption_str = "1=1"

        if in_a_condo is True:
            self.in_a_condo_str = "in_condo = 1"
        elif in_a_condo is False:
            self.in_a_condo_str = "in_condo = 0"
        elif in_a_condo is None:
            self.in_a_condo_str = "1=1"

    @property
    def query(self):
        return f"""
        SELECT 
            'no-rental-license' as type,
            location, unit, num_units, category_code_description, num_unique_owners, owner_most_ownership, likely_owner_occupied, other_info, parcel_number, zip_code,
            ST_Y(the_geom) AS lat, ST_X(the_geom) AS lng 
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
                group by
                  the_geom
              ) col
            where
                {self.in_a_condo_str}
                and {self.building_type_str}
                and {self.homestead_exemption_str}
                and {self.where_str}
            order by
              {self.order_by_str}
              {self.limit_str}
        """


class NeighborhoodRentalLicenseQuery(NeighborhoodQuery):
    def __init__(
        self,
        rental_building_types: list[str],
        is_owner_occupied: bool,
        where_str: str,
        order_by_str: str,
        n_results: int,
    ):
        super().__init__(
            n_results=n_results, where_str=where_str, order_by_str=order_by_str
        )
        """
        self.rental_building_type_str = ",".join(
            [f"'{build_type}'" for build_type in rental_building_types.split(",")]
        )
        """
        if is_owner_occupied is True:
            self.owner_occupied_str = "owneroccupied = 'No'"
        elif is_owner_occupied is False:
            self.owner_occupied_str = "owneroccupied = 'Yes'"
        elif is_owner_occupied is None:
            self.owner_occupied_str = "1=1"

    @property
    def query(self):
        return f"""
        select * from (
            select
              the_geom,
              opa_account_num as parcel_number,
              address as location,
              zip_code,
              'has-rental-license' as type,
              CASE WHEN numberofunits > 1 THEN '' ELSE unit_num END as unit,
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
              owneroccupied as likely_owner_occupied,
              ST_Y(the_geom) AS lat, ST_X(the_geom) AS lng
            from
              (select left(zip,5) as zip_code, * from business_licenses) bl
            where
              licensestatus = 'Active'
              and licensetype = 'Rental'
              and {self.owner_occupied_str}
            ) subquery WHERE
              {self.where_str}
            ORDER BY {self.order_by_str}
              {self.limit_str}
        """


def get_walk_list_order(df, starting_lat, starting_lng):
    def populate(lat_lis, lon_lis, r=3958.75):
        lat_mtx = np.array([lat_lis]).T * np.pi / 180
        lon_mtx = np.array([lon_lis]).T * np.pi / 180

        cos_lat_i = np.cos(lat_mtx)
        cos_lat_j = np.cos(lat_mtx)
        cos_lat_J = np.repeat(cos_lat_j, len(lat_mtx), axis=1).T

        lat_Mtx = np.repeat(lat_mtx, len(lat_mtx), axis=1).T
        cos_lat_d = np.cos(lat_mtx - lat_Mtx)

        lon_Mtx = np.repeat(lon_mtx, len(lon_mtx), axis=1).T
        cos_lon_d = np.cos(lon_mtx - lon_Mtx)

        mtx = r * np.arccos(cos_lat_d - cos_lat_i * cos_lat_J * (1 - cos_lon_d))
        return mtx

    dist_matrix = populate(
        list(df.lat.values) + [float(starting_lat)],
        list(df.lng.values) + [float(starting_lng)],
    )

    df_dist = pd.DataFrame(
        dist_matrix,
        columns=list(df.location.values) + ["starting_place"],
        index=list(df.location.values) + ["starting_place"],
    )
    df_dist.index.name = "start"
    df_dist = df_dist.reset_index().melt(
        id_vars=["start"], value_vars=df.location.values
    )
    df_dist.columns = ["start", "end", "distance"]

    walk_list = []
    remaining_df = df_dist.copy()

    next_stop = "starting_place"
    remaining_df = remaining_df[remaining_df.end != next_stop]
    while len(remaining_df) > 0:
        next_stop_index = remaining_df[
            remaining_df["start"] == next_stop
        ].distance.idxmin()
        next_stop = remaining_df.loc[next_stop_index].end
        walk_list.append(next_stop)
        remaining_df = remaining_df[remaining_df.end != next_stop]

    walk_list_df = df.set_index("location").loc[walk_list].reset_index()
    walk_list_df.index.name = "walk_order"
    walk_list_df = walk_list_df.reset_index()
    return walk_list_df
