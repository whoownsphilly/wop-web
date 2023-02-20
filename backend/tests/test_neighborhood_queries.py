import pandas as pd
from passyunk.parser import PassyunkParser
from backend.queries.neighborhood_queries import (
    properties_by_organizability_results,
    get_walk_list_order,
)


async def test_walklist():
    results = await properties_by_organizability_results(
        northeast_lat=None,
        southwest_lat=None,
        northeast_lng=None,
        southwest_lng=None,
        zip_code=19103,
        starting_latitude=None,
        starting_longitude=None,
        search_by="zipCode",
        license_filter="",
        owner_occupied_filter="",
        condo_filter="",
        building_types="Multi Family",
        rental_building_types="Residential Dwelling",
        num_lists=10,
        num_units_per_list=10,
    )
    df = pd.DataFrame(results["searched_properties"])
    starting_place = df.iloc[0]

    df = get_walk_list_order(
        df, starting_lat=starting_place.lat, starting_lng=starting_place.lng
    )
    assert not df.empty
