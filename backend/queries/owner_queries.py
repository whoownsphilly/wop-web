from datetime import datetime
import numpy as np
import pandas as pd

from backend.queries.manual_queries import MANUAL_MAILING_ADDRESS_QUERIES
from backend.queries.queries import carto_request, DEEDS_WHERE_CLAUSE


def _run_sql_on_df(df, query, table_name, file_name="test.sql"):
    import sqlite3
    import os
    import tempfile

    tmp_path = tempfile.mkdtemp()
    con = sqlite3.connect(os.path.join(tmp_path, file_name))
    df.to_sql(table_name, con=con, index=False)
    return pd.read_sql(query, con=con)


def _get_current_properties_from_timeline(timeline_df):
    current_timeline_df = timeline_df.query("current_owner==True")

    return (
        current_timeline_df.groupby(current_timeline_df.index)[
            "market_value", "lat", "lng", "location_unit"
        ]
        .first()
        .reset_index()
    )


def _get_owner_list_subquery(owner_subquery, return_parcel_number=False):
    """Get list of owner names as:
    - rtt_summary.grantees
        - WHERE it is a DEED and name is found inside of the owner name
        - TO-DO: Check if this is mis-grouping shorter names with longer ones?
    - business_licenses.business_name
        - WHERE it is a Rental license and name in business_name or legalname
    - business_licenses.legalname
        - WHERE it is a Rental license and name in business_name or legalname
    - opa_properties_public.mailing_care_of
        - WHERE name in owner_1, owner_2, or mailing_care_of
    - opa_properties_public.owner_1
        - WHERE name in owner_1, owner_2, or mailing_care_of
    - opa_properties_public.owner_2
        - WHERE name in owner_1, owner_2, or mailing_care_of
    - opa_properties_public.owner_1;opa_properties_public.owner_2
        - WHERE name in owner_1, owner_2, or mailing_care_of
        - This is to match the grantees field which is semi-colon separated names
    """

    '''
    # includes too many lines of query
    return f"""
        SELECT grantees as names, 
         {'opa_account_num,' if return_parcel_number else ''}
         'grantees' as source
         FROM rtt_summary 
         WHERE ({DEEDS_WHERE_CLAUSE})
         AND grantees in ({owner_subquery})
         UNION ALL
         SELECT business_name as names, 
         {'opa_account_num,' if return_parcel_number else ''}
         'business_name' as source
         FROM business_licenses WHERE licensetype = 'Rental'
         AND legalname in ({owner_subquery}) or business_name in ({owner_subquery})
         UNION ALL
         SELECT legalname as names,
         {'opa_account_num,' if return_parcel_number else ''}
         'legalname' as source
         FROM business_licenses WHERE licensetype = 'Rental'
         AND legalname in ({owner_subquery}) or business_name in ({owner_subquery})
         UNION ALL
         SELECT mailing_care_of as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'mailing_care_of' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         AND mailing_care_of is not null
         UNION ALL
         SELECT owner_1 as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_1' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         UNION ALL
         SELECT owner_2 as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_2' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         and owner_2 is not null
         UNION ALL
         SELECT concat(owner_1,'; ',owner_2) as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_1;owner_2' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         and owner_2 is not null
    """
    '''

    # This is if we want to include OPA owner fields, but they can be outdated and the names should be in the deeds already, so we shouldn't need this.
    """
         UNION ALL
         SELECT owner_1 as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_1' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         UNION ALL
         SELECT owner_2 as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_2' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         and owner_2 is not null
         UNION ALL
         SELECT concat(owner_1,'; ',owner_2) as names,
         {'parcel_number as opa_account_num,' if return_parcel_number else ''}
         'owner_1;owner_2' as source
         FROM opa_properties_public 
         WHERE (
           owner_1 in ({owner_subquery}) or owner_2 in ({owner_subquery})
           OR mailing_care_of in ({owner_subquery})
         )
         and owner_2 is not null
    """

    return f"""
        SELECT grantees as names, 
         {'opa_account_num,' if return_parcel_number else ''}
         'grantees' as source
         FROM rtt_summary 
         WHERE ({DEEDS_WHERE_CLAUSE})
         AND grantees in ({owner_subquery})
         UNION ALL
         SELECT business_name as names, 
         {'opa_account_num,' if return_parcel_number else ''}
         'business_name' as source
         FROM business_licenses WHERE licensetype = 'Rental'
         AND legalname in ({owner_subquery}) or business_name in ({owner_subquery})
         UNION ALL
         SELECT legalname as names,
         {'opa_account_num,' if return_parcel_number else ''}
         'legalname' as source
         FROM business_licenses WHERE licensetype = 'Rental'
         AND legalname in ({owner_subquery}) or business_name in ({owner_subquery})
    """


def _get_property_counts_by_name_chart_input(owner_property_counts_by_name):
    # Get property counts by name for apex grouped bar chart in format:
    # x: {'name': 'currently owned', 'data': [1,2]}
    # y: [ownername1, ownername2, ownername3]
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
    return {
        "categories": chart_categories,
        "data": chart_data,
    }


def properties_by_owner_name_results(parcel_number):
    # 2021-12-01
    # This is repetitive, but get owner name from parcel_number
    # This doesn't handle the case where deeds changed but
    # the opa_properties_public table hasn't been updated.
    # In this case, it includes both the latest owners in the
    # opa_properties_public table as well as the latest deed
    # owners. This is wrong but we'll have to fix it later.
    # UPDATE (2022-01-09)
    # I am just going to base it off of the latest DEED.
    """
    owner_subquery = f'''
        WITH  owner_options as (
        SELECT grantees, owner_1, owner_2
            FROM opa_properties_public opa_inner
            LEFT JOIN (
                SELECT * FROM rtt_summary
                WHERE ({DEEDS_WHERE_CLAUSE})
                AND opa_account_num = '{parcel_number}'
                ORDER BY recording_date desc limit 1
            ) rtt
            ON rtt.opa_account_num = opa_inner.parcel_number
            AND rtt.recording_date >= opa_inner.recording_date
            WHERE opa_inner.parcel_number = '{parcel_number}'
        )
        SELECT grantees as owner_name
        FROM owner_options WHERE grantees is not null
        --UNION ALL
        --SELECT owner_1 as owner_name
        --FROM owner_options where owner_1 is not null
        --UNION ALL
        --SELECT owner_2 as owner_name
        --FROM owner_options
        --WHERE owner_2 is not null
    '''
    this_property_owner_list = list(
        set([x["owner_name"] for x in carto_request(owner_subquery, as_df=False)])
    )
    # TODO (possibly split by ;)
    this_property_owner_str = ",".join([f"'{x}'" for x in this_property_owner_list])

    #owner_subquery = _get_owner_list_subquery(this_property_owner_str, True)

    # This would give a timeline of properties (including those
    # that the owner no longer owns
    owners_list = carto_request(
        f"SELECT distinct names from ({owner_subquery}) name_list"
    )
    from phillydb.owner_search_queries import OwnerQueryResult
    owner_query_result_obj = OwnerQueryResult(
        f"SELECT opa_account_num FROM ({owner_subquery}) owner_list",
        [x["names"] for x in owners_list],
    )
    owner_property_timeline_df = owner_query_result_obj.owners_timeline_df
    owner_property_timeline_df.rename(
        columns={"parcel_number": "opa_account_num"}, inplace=True
    )
    """
    # We are for now just going to get properties the owner currently is
    # associated with.

    inner_query = f"""
        SELECT grantees as names, opa_account_num FROM rtt_summary 
         WHERE 
         ({DEEDS_WHERE_CLAUSE})
         AND grantees in (
            SELECT grantees
            FROM opa_properties_public opa_inner
            LEFT JOIN (
                SELECT * FROM rtt_summary
                WHERE ({DEEDS_WHERE_CLAUSE})
                AND opa_account_num = '{parcel_number}'
                ORDER BY recording_date desc limit 1
            ) rtt
            ON rtt.opa_account_num = opa_inner.parcel_number
            AND rtt.recording_date >= opa_inner.recording_date
            WHERE opa_inner.parcel_number = '{parcel_number}'
        )
    """

    joined_inner_query = f" JOIN ({inner_query}) owner_list ON owner_list.opa_account_num = opa.parcel_number"

    def _deeds_query(inner_query):
        return f"""
         SELECT 
        rtt_summary.property_count,
        rtt_summary.grantees as likely_owner, 
        rtt_summary2.grantees as sold_to, 
        rtt_summary.document_date as start_dt,
        CASE WHEN (rtt_summary.document_date is null) THEN rtt_summary.recording_date ELSE rtt_summary.document_date END as start_dt,
        rtt_summary2.document_date as end_dt,
        opa.parcel_number as opa_account_num,
        opa.location as opa_address,
        unit as opa_address_unit,
        concat_ws(
            ' ', 
            address_low, 
            address_low_suffix, 
            address_low_frac, 
            address_high, 
            street_predir, 
            rtt_summary.street_name, 
            street_suffix, 
            street_postdir
        ) as address, 
        opa.location,
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        opa.unit,
        opa.mailing_street, 
        opa.mailing_address_1, 
        opa.mailing_address_2, 
        opa.mailing_city_state, 
        opa.mailing_zip, 
        opa.mailing_care_of,
        opa.market_value,
        opa.recording_date as opa_recording_date,
        CASE WHEN (rtt_summary.opa_account_num is null) THEN 'opa_properties_public' ELSE 'rtt_summary' END as source
        FROM
        opa_properties_public opa
        -- get when it was bought by joining on grantees
        -- sometimes the deeds dont match. Making this a LEFT join may mean
        -- additional properties get pulled in
        LEFT JOIN (
            SELECT * FROM rtt_summary  WHERE ({DEEDS_WHERE_CLAUSE})
        ) rtt_summary
        ON rtt_summary.recording_date =  opa.recording_date
        AND rtt_summary.opa_account_num = opa.parcel_number
        -- get when it was sold by joining the grantee to the grantor
        LEFT JOIN (
            SELECT opa_account_num, grantors, grantees, recording_date, document_date
            FROM rtt_summary  WHERE ({DEEDS_WHERE_CLAUSE})
        ) rtt_summary2
        ON rtt_summary.grantees = rtt_summary2.grantors
        AND rtt_summary2.opa_account_num = opa.parcel_number
        AND rtt_summary.recording_date < rtt_summary2.recording_date
        {inner_query}
        WHERE opa.category_code_description not in ('Commercial', 'Industrial','Vacant Land')
       """

    property_timeline_df = carto_request(_deeds_query(joined_inner_query))
    # TODO (We should only be returning a single row now since it should be
    # the most recent owner only
    # so we can possibly simplify the logic below

    # If the last row doesn't have a null entry in end_dt (like with 881074500) we can manually add one. I'm not exactly sure why this happened.
    property_timeline_df.sort_values("end_dt", inplace=True)
    if not property_timeline_df.empty and not pd.isnull(
        property_timeline_df.iloc[-1]["end_dt"]
    ):
        last_row = property_timeline_df.iloc[-1]
        new_row = last_row.copy()
        new_row["likely_owner"] = last_row["sold_to"]
        new_row["start_dt"] = last_row["end_dt"]
        new_row["end_dt"] = None
        property_timeline_df = property_timeline_df.append(new_row)

    # Limit to only owners that had matched the owner list
    # This would be unnecessary if we could join the opa data to a grantee, but the owner_1-owner_2 <-> grantee mapping is unreliable
    distinct_owner_names = carto_request(
        f"SELECT DISTINCT names from ({inner_query}) owner_names"
    )
    owner_property_timeline_df = property_timeline_df[
        property_timeline_df.likely_owner.isin(distinct_owner_names["names"].values)
    ]

    # Manipulations on the owner df

    # TODO Better handling of properties with multiple addresses
    # For example, corner properties return multiple rows.
    # For now, we are just dropping those duplicate properties
    # But in the future we will want to display these "alternate addresses"
    owner_property_timeline_df.drop_duplicates("opa_account_num", inplace=True)

    # The query used to return properties that the owner didnt currently own
    # but we have since changed that. So this should always be True.
    # unless they previously owned a property, sold, and rebought.
    owner_property_timeline_df["current_owner"] = pd.isnull(
        owner_property_timeline_df["end_dt"]
    )
    owner_property_timeline_df.set_index("opa_account_num", inplace=True)
    owner_property_timeline_df = owner_property_timeline_df.replace({np.nan: None})

    owner_property_timeline_df["location_unit"] = (
        owner_property_timeline_df["location"]
        + " "
        + owner_property_timeline_df["unit"].fillna("")
    ).str.strip()

    # Also lets get rid of the constructed address field for now
    owner_property_timeline_df.drop("address", axis=1, inplace=True)

    # Add n_days column (lesser of since they bought or the since_date
    analysis_since_date = "2007-01-01"
    owner_property_timeline_df = calculate_n_days_property_ownership(
        owner_property_timeline_df, since_date=analysis_since_date
    )

    owner_property_timeline_df = _add_violation_counts(
        joined_inner_query, owner_property_timeline_df, analysis_since_date
    )
    owner_property_timeline_df = _add_complaint_counts(
        joined_inner_query, owner_property_timeline_df, analysis_since_date
    )
    owner_property_timeline_df["color"] = "red"

    owner_property_counts_by_name = (
        owner_property_timeline_df.groupby(["likely_owner", "current_owner"])
        .size()
        .to_frame("n_properties")
        .reset_index()
    )
    alias_names = list(
        set(
            (
                owner_property_timeline_df["mailing_care_of"]
                .drop_duplicates()
                .dropna()
                .values.tolist()
                + owner_property_timeline_df["likely_owner"]
                .drop_duplicates()
                .dropna()
                .values.tolist()
            )
        )
    )

    # The timeline and the "currently owned" list could be done separately
    # but we'll keep them grouped for now
    current_properties = _get_current_properties_from_timeline(
        owner_property_timeline_df
    )
    current_properties["color"] = "red"

    return {
        "results": {
            "alias_names": alias_names,
            "timeline": owner_property_timeline_df.rename_axis("opa_account_num")
            .reset_index()
            .to_dict("records"),
            "property_counts": owner_property_counts_by_name,
            "current_properties": current_properties,
        },
        "display_inputs": {
            "owner_property_counts_by_name": _get_property_counts_by_name_chart_input(
                owner_property_counts_by_name
            ),
        },
        "query": inner_query,
        "metadata": {"parcel_number": parcel_number},
    }


def _inner_mailing_address_join_query(mailing_address_query):
    # Might not be totally accurate as some recording_dates haven't been updated
    # since 2016 (like 172480000) even though a new transaction took place
    # so the mailing addresses might actually be outdated
    return f"""JOIN ({mailing_address_query}) opa2 ON opa.mailing_street = opa2.mailing_street
        AND (
              opa.mailing_address_1 = opa2.mailing_address_1
              OR (opa.mailing_address_1 is null and opa2.mailing_address_1 is null)
        )
        """


def properties_by_mailing_address_results(parcel_number):

    ## This might add unnecessary length to the query, but will give it a try:
    ## We're going to do a quick request to check the mailing address for this parcel number
    def _get_inner_query(parcel_number, manual_queries):
        mailing_address = carto_request(
            f"""SELECT mailing_street, mailing_address_1, mailing_address_2, mailing_care_of, owner_1, owner_2,location from 
            opa_properties_public where parcel_number = '{parcel_number}'
            """
        )
        inner_query = _inner_mailing_address_join_query(parcel_number)
        for query_name, query in manual_queries.items():
            # If it is in one of the manual queries, then use that extended query
            if not _run_sql_on_df(
                mailing_address, query, "opa_properties_public"
            ).empty:
                return query_name, _inner_mailing_address_join_query(query)
        # else return a query that simply joins on the exact mailing address
        query = f"""SELECT mailing_street, 
                mailing_address_1
                 FROM opa_properties_public
                WHERE parcel_number = '{parcel_number}'
                GROUP BY mailing_street, mailing_address_1
                """
        return None, _inner_mailing_address_join_query(query)

    query_name, joined_inner_query = _get_inner_query(
        parcel_number, MANUAL_MAILING_ADDRESS_QUERIES
    )

    """
    Notes: The city's rtt_summary.property count is doing a:
    '''
    p_count.property_count,
    ...
    JOIN (SELECT document_id, count(*) as property_count 
    from rtt_summary group by document_id) p_count
    ON rtt_summary.document_id = p_count.document_id 

    so you need to be careful to join to the right DEED in order to get the right count
    """

    def _mailing_address_deeds_query(inner_query):
        return f"""
        SELECT DISTINCT * FROM (
         SELECT 
        rtt_summary.property_count,
        rtt_summary.grantees as likely_owner, 
        rtt_summary2.grantees as sold_to, 
        rtt_summary.document_date as start_dt,
        rtt_summary2.document_date as end_dt,
        rtt_summary.document_id,
        opa.parcel_number as opa_account_num,
        opa.location as opa_address,
        unit as opa_address_unit,
        concat_ws(
            ' ', 
            address_low, 
            address_low_suffix, 
            address_low_frac, 
            address_high, 
            street_predir, 
            rtt_summary.street_name, 
            street_suffix, 
            street_postdir
        ) as address, 
        opa.location,
        ST_Y(opa.the_geom) AS lat, ST_X(opa.the_geom) AS lng,
        opa.unit,
        opa.mailing_street, 
        opa.mailing_address_1, 
        opa.mailing_address_2, 
        opa.mailing_city_state, 
        opa.mailing_zip, 
        opa.mailing_care_of,
        opa.market_value,
        CASE WHEN (rtt_summary.opa_account_num is null) THEN 'opa_properties_public' ELSE 'rtt_summary' END as source
        FROM
        opa_properties_public opa
        -- get when it was bought by joining on grantees
        -- sometimes the deeds dont match. Making this a LEFT join may mean
        -- additional properties get pulled in
        LEFT JOIN (
            SELECT * FROM rtt_summary  WHERE ({DEEDS_WHERE_CLAUSE})
        ) rtt_summary
        ON rtt_summary.recording_date =  opa.recording_date
        AND rtt_summary.opa_account_num = opa.parcel_number
        -- get when it was sold by joining the grantee to the grantor
        LEFT JOIN (
            SELECT opa_account_num, grantors, grantees, recording_date, document_date
            FROM rtt_summary  WHERE ({DEEDS_WHERE_CLAUSE})
        ) rtt_summary2
        ON rtt_summary.grantees = rtt_summary2.grantors
        AND rtt_summary2.opa_account_num = opa.parcel_number
        AND rtt_summary.document_date <= rtt_summary2.document_date
        {inner_query}
        WHERE opa.category_code_description not in ('Commercial', 'Industrial','Vacant Land')
        ) distinct_replies
       """

    query = _mailing_address_deeds_query(joined_inner_query)
    ma_property_timeline_df = carto_request(query)
    if ma_property_timeline_df.empty:
        # Temporary hack to get back its own address
        # This is usually needed if mailing address fields
        # are empty.
        # TODO (properly handle empty mailing_street case)
        joined_inner_query = f"""
            JOIN (
                SELECT mailing_street, mailing_address_1, parcel_number 
                FROM opa_properties_public 
                WHERE parcel_number = '{parcel_number}'
            ) opa2 on opa.parcel_number = opa2.parcel_number
        """
        query = _mailing_address_deeds_query(joined_inner_query)
        ma_property_timeline_df = carto_request(query)

    # Also lets get rid of the constructed address field for now otherwise we end up with duplicates
    ma_property_timeline_df.drop("address", axis=1, inplace=True)

    # drop duplicates and set index (take later document_id, example: 341182500 with two deeds on the same day 2010-02-23)
    cols = [
        c
        for c in ma_property_timeline_df.columns
        if c not in ["document_id", "likely_owner"]
    ]
    ma_property_timeline_df = ma_property_timeline_df.sort_values(
        "document_id"
    ).drop_duplicates(subset=cols, keep="last")
    ma_property_timeline_df = ma_property_timeline_df.sort_values(
        ["opa_account_num", "start_dt"]
    ).set_index("opa_account_num")
    ma_property_timeline_df["current_owner"] = pd.isnull(
        ma_property_timeline_df["end_dt"]
    )
    # For now, only send out ones with the "current owner"
    ma_property_timeline_df = ma_property_timeline_df[
        ma_property_timeline_df["current_owner"] == True
    ]

    ma_property_timeline_df["location_unit"] = (
        ma_property_timeline_df["location"]
        + " "
        + ma_property_timeline_df["unit"].fillna("")
    ).str.strip()

    ma_property_timeline_df["end_dt"] = (
        pd.to_datetime(ma_property_timeline_df["end_dt"])
        .fillna(pd.to_datetime(datetime.now()))
        .apply(lambda x: x.date())
    )
    # Add n_days column (lesser of since they bought or the since_date)
    analysis_since_date = "2007-01-01"
    ma_property_timeline_df = _add_violation_counts(
        joined_inner_query, ma_property_timeline_df, analysis_since_date
    )
    ma_property_timeline_df = _add_complaint_counts(
        joined_inner_query, ma_property_timeline_df, analysis_since_date
    )

    mailing_address_str = " ".join(
        ma_property_timeline_df[
            [
                "mailing_street",
                "mailing_address_1",
                "mailing_address_2",
                "mailing_city_state",
                "mailing_zip",
            ]
        ]
        .iloc[0]
        .dropna()
        .values
    )
    # get timeline with purchased and sold date cols by property
    ma_property_timeline_df["color"] = "yellow"

    owner_property_counts_by_name = (
        ma_property_timeline_df.groupby(["likely_owner", "current_owner"])
        .size()
        .to_frame("n_properties")
        .reset_index()
    )
    current_properties = _get_current_properties_from_timeline(ma_property_timeline_df)
    alias_names = list(
        set(
            (
                ma_property_timeline_df["mailing_care_of"]
                .drop_duplicates()
                .dropna()
                .values.tolist()
                + ma_property_timeline_df["likely_owner"]
                .drop_duplicates()
                .dropna()
                .values.tolist()
            )
        )
    )
    current_properties["color"] = "yellow"
    current_properties["source"] = "mailing_address"

    output = {
        "results": {
            "alias_names": alias_names,
            "timeline": ma_property_timeline_df.rename_axis(
                "opa_account_num"
            ).reset_index(),
            "property_counts": owner_property_counts_by_name,
            "current_properties": current_properties,
        },
        "display_inputs": {
            "owner_property_counts_by_name": _get_property_counts_by_name_chart_input(
                owner_property_counts_by_name
            ),
        },
        "query": query,
        "metadata": {
            "query_name": query_name,
            "parcel_number": parcel_number,
            "mailing_address": mailing_address_str,
        },
    }
    return output


def _add_complaint_counts(inner_query, timeline_df, analysis_since_date):
    violations_query = f"""
     SELECT distinct comp.opa_account_num, complaintdate, complaintnumber
     FROM opa_properties_public opa
     {inner_query}
     JOIN complaints comp
     ON opa.parcel_number = comp.opa_account_num
     WHERE comp.complaintdate > '{analysis_since_date}'
    """
    complaints = carto_request(violations_query)
    timeline_df["start_dt"] = pd.to_datetime(timeline_df["start_dt"]).dt.date
    complaints["complaintdate"] = pd.to_datetime(complaints["complaintdate"]).dt.date
    comp_timeline_df = timeline_df.join(
        complaints.set_index("opa_account_num"), how="inner"
    )
    comp_timeline_df_filtered = (
        comp_timeline_df[
            (comp_timeline_df.complaintdate >= comp_timeline_df.start_dt)
            & (
                (comp_timeline_df.complaintdate <= comp_timeline_df.end_dt)
                | (pd.isnull(comp_timeline_df.end_dt))
            )
        ]
        .rename_axis("opa_account_num")
        .reset_index()
    )

    timeline_df = timeline_df.join(
        comp_timeline_df_filtered["opa_account_num"]
        .value_counts()
        .rename("n_complaints"),
        how="left",
    ).fillna({"n_complaints": 0})
    return timeline_df


def _add_violation_counts(inner_query, timeline_df, analysis_since_date):
    violations_query = f"""
     SELECT distinct vio.opa_account_num, violationnumber, vio.cartodb_id, violationdate, caseprioritydesc, violationstatus, violationcodetitle, violationresolutioncode
     FROM opa_properties_public opa
     {inner_query}
     JOIN violations vio
     ON opa.parcel_number = vio.opa_account_num
     WHERE vio.violationdate > '{analysis_since_date}'
    """
    violations = carto_request(violations_query)
    timeline_df["start_dt"] = pd.to_datetime(timeline_df["start_dt"]).dt.date
    violations["violationdate"] = pd.to_datetime(violations["violationdate"]).dt.date
    vio_timeline_df = timeline_df.join(
        violations.set_index("opa_account_num"), how="inner"
    )
    vio_timeline_df_filtered = vio_timeline_df[
        (vio_timeline_df.violationdate >= vio_timeline_df.start_dt)
        & (
            (vio_timeline_df.violationdate <= vio_timeline_df.end_dt)
            | (pd.isnull(vio_timeline_df.end_dt))
        )
    ].reset_index()

    timeline_df = timeline_df.join(
        vio_timeline_df_filtered["opa_account_num"]
        .value_counts()
        .rename("n_violations"),
        how="left",
    ).fillna({"n_violations": 0})
    timeline_df = timeline_df.join(
        vio_timeline_df_filtered[vio_timeline_df_filtered.violationstatus == "OPEN"][
            "opa_account_num"
        ]
        .value_counts()
        .rename("n_violations_open"),
        how="left",
    ).fillna({"n_violations_open": 0})
    timeline_df = timeline_df.join(
        vio_timeline_df_filtered[vio_timeline_df_filtered.violationstatus != "OPEN"][
            "opa_account_num"
        ]
        .value_counts()
        .rename("n_violations_closed"),
        how="left",
    ).fillna({"n_violations_closed": 0})

    # pass violation_text as json object
    # TODO, return the violations list and the link to the violations
    # so it can easily be clicked on when they appear.
    """
    def _generate_json(violations_per_property):
        return [
            f"{x.violationdate} ({x.opa_account_num}), Priority: {x.caseprioritydesc}, Violation: {x.violationcodetitle} Status: {x.violationstatus}"
            for index, x in violations_per_property.iterrows()
        ]

    violation_json = (
        vio_timeline_df_filtered.groupby(vio_timeline_df_filtered.opa_account_num)
        .apply(_generate_json)
        .rename("violation_json")
    )
    timeline_df = timeline_df.join(violation_json, how="left")
    """
    return timeline_df


def calculate_n_days_property_ownership(df, since_date):
    """
    We need n_days to be the lesser of the difference between end_dt
    """
    df["start_range"] = pd.to_datetime(since_date).date()
    df["end_dt"] = (
        pd.to_datetime(df["end_dt"])
        .fillna(pd.to_datetime(datetime.now()))
        .apply(lambda x: x.date())
    )
    df["start_dt"] = pd.to_datetime(df["start_dt"]).apply(lambda x: x.date())

    df["n_days_owned"] = (df["end_dt"] - df["start_dt"]).dt.days
    df["n_days_since_range"] = (df["end_dt"] - df["start_range"]).dt.days
    df["n_days"] = df[["n_days_since_range", "n_days_owned"]].min(axis=1)
    return df
