from backend.queries.queries import carto_request, DEEDS_WHERE_CLAUSE, airtable_request
from fuzzywuzzy import fuzz
import pandas as pd
from phillydb.utils import get_normalized_address
from scourgify.exceptions import UnParseableAddressError


def property_latest_owner_detail_results(parcel_number):
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
            WHERE ({DEEDS_WHERE_CLAUSE})
            AND opa_account_num='{parcel_number}' 
            ORDER by recording_date DESC limit 1
        ) latest_owners
        FULL JOIN opa_properties_public opa
        ON latest_owners.opa_account_num = opa.parcel_number
        WHERE opa.parcel_number='{parcel_number}'
    """
    data = carto_request(query, as_df=False)
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

        # output["crowd_sourced"] = airtable_request(mailing_street, mailing_address_1)
        output["query"] = query
    else:
        output = {"success": False}
    return output


def property_page_results(parcel_number, violations_complaints_date_since="2007-01-01"):
    output = {}
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
        n_violations_open, n_violations_closed_since,
        n_complaints_since,
        has_active_rental_license, 
        expiration_date as rental_license_expiration_date, 
        numberofunits as number_of_licensed_rental_units,
        r1.recording_date, r1.grantees, r1.grantors, r1.cash_consideration, r1.property_count as n_properties_on_deed,
        a1.market_value as latest_assessment_market_value, a1.latest_assessment_year
        FROM opa_properties_public opp
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_violations_open
            FROM violations
            WHERE opa_account_num = '{parcel_number}'
            AND violationstatus = 'OPEN'
        ) v_open
        ON opp.parcel_number = v_open.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_violations_closed_since
            FROM violations
            WHERE opa_account_num = '{parcel_number}'
            --AND caseprioritydesc in ('HAZARDOUS', 'UNSAFE', 'IMMINENTLY DANGEROUS')
            AND violationdate >= '{violations_complaints_date_since}'
            AND violationstatus != 'OPEN'
        ) v_closed
        ON opp.parcel_number = v_closed.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number, count(*) as n_complaints_since
            FROM complaints
            WHERE opa_account_num = '{parcel_number}'
            AND complaintdate >= '{violations_complaints_date_since}'
        ) complaints
        ON opp.parcel_number = complaints.parcel_number
        LEFT JOIN (
            SELECT '{parcel_number}' as parcel_number,
            CASE WHEN count(*) > 0 THEN TRUE ELSE FALSE END as has_active_rental_license,
            sum(numberofunits) as numberofunits,
            max(expirationdate) as expiration_date
            FROM business_licenses
            WHERE opa_account_num = '{parcel_number}'
            AND licensetype='Rental'
            AND licensestatus='Active'
        ) l1
        ON opp.parcel_number = l1.parcel_number
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
        ON opp.parcel_number = r1.parcel_number
        LEFT JOIN (
            SELECT parcel_number,
            year as latest_assessment_year,
            market_value
            FROM assessments a
            WHERE parcel_number = '{parcel_number}'
            ORDER BY year DESC LIMIT 1
        ) a1
        ON opp.parcel_number = a1.parcel_number
        WHERE opp.parcel_number = '{parcel_number}'
        """

    data = carto_request(query, as_df=False)

    if len(data) > 0:
        output.update(data[0])
    return output


def property_details_page_results(parcel_number):
    output = {}
    # PROPERTY TIMELINE AND VALUE LIST
    query = f"""
    SELECT * FROM (
        SELECT 
        'purchased' as status, 
        opa_account_num as parcel_number,
        grantees as owner, 
        grantors as seller,
        cash_consideration as property_value, 
        document_date as date
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
    assessment_timeline_data = carto_request(query, as_df=False)
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
        owner_data = []
        if "owner_1" in output:
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
    output["query"] = query
    return output


def properties_by_autocomplete_results(
    startswith_str, n_results=10, min_search_length=4
):
    if len(startswith_str) < min_search_length:
        return {
            "success": False,
            "results": {},
            "query": "",
            "metadata": {"search_to_match": search_to_match},
        }
    else:
        results = properties_by_property_autocomplete_results(startswith_str, n_results)
    if results:
        return results
    else:
        return properties_by_owner_name_autocomplete_results(startswith_str, n_results)


def properties_by_owner_name_autocomplete_results(owner_substr, n_results):
    search_to_match_like_str = "%".join(owner_substr.split(" ")).upper()
    search_to_match_like_str_rev = "%".join(owner_substr.split(" ")[::-1]).upper()
    query = f"""
        SELECT location, unit, 
        CASE 
            WHEN grantees is null 
            THEN concat_ws('; ', owner_1, owner_2) 
            ELSE grantees 
        END as grantees, 
        parcel_number as opa_account_num FROM
        opa_properties_public LEFT JOIN
        (
             SELECT grantees, rtt_inner.opa_account_num from rtt_summary 
            JOIN (
                SELECT max(document_id) as document_id, opa_account_num
                FROM rtt_summary
                WHERE (
                  document_type='DEED' OR
                  document_type='DEED SHERIFF' OR
                  document_type='DEED OF CONDEMNATION' OR
                  document_type='DEED LAND BANK'

                )
                AND (
                    grantees like '%{search_to_match_like_str}%'
                    OR grantees like '%{search_to_match_like_str_rev}%'
                )
                GROUP by opa_account_num
                
                ) rtt_inner 
            ON rtt_inner.document_id = rtt_summary.document_id
        ) rtt
        ON opa_properties_public.parcel_number = rtt.opa_account_num
        WHERE ( 
            grantees like '%{search_to_match_like_str}%'
            OR grantees like '%{search_to_match_like_str_rev}%'
            OR mailing_care_of like '%{search_to_match_like_str}%'
        )
        AND
        parcel_number is not null
        LIMIT {n_results} 
    """
    df = carto_request(query)
    df = df.groupby("opa_account_num").first().reset_index()

    df["location_unit"] = (df["location"] + " " + df["unit"].fillna("")).str.strip()

    df["parcel_number"] = df["opa_account_num"]
    df["description"] = df["grantees"]
    return {
        "success": True,
        "results": df.to_dict("records"),
        "query": query,
        "metadata": {"search_to_match": owner_substr, "n_results": n_results},
    }


def properties_by_property_autocomplete_results(property_substr, n_results):

    try:
        search_to_match = get_normalized_address(property_substr)
    except UnParseableAddressError:
        return
    search = search_to_match.split(" ")
    # This more complicated SQL allows for things like
    # 1850 ABC St, 1846 ABC St, and 1840 ABC St
    # to all be captured if a property is labelled internally
    # as 1844-1850 ABC St
    includes_dir = len(search) > 1 and search[1] in ["N", "S", "E", "W"]
    first_word_split = search[0].split("-")
    address_low = int("".join(x for x in first_word_split[0] if x.isdigit()).strip())
    address_low_suffix = "".join(
        x for x in first_word_split[0] if not x.isdigit()
    ).strip()
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
    address_low_suffix_str = (
        f"AND address_low_suffix like '%{address_low_suffix}%'"
        if address_low_suffix
        else ""
    )
    unit_str = f"AND unit_num LIKE '%{unit}%'" if unit else ""
    street_dir_str = (
        f"AND (street_predir LIKE '%{search[1]}%' OR street_postdir LIKE '%{search[1]}%')"
        if includes_dir
        else ""
    )

    query = f"""
    SELECT distinct location, opa_account_num, 
    --WARNING mailing addresses may not line up with the newest owners if OPA table is outdated
    grantees,
    mailing_address_1, mailing_address_2, mailing_care_of, 
    CAST(opa_properties_public.recording_date as TEXT) as mailing_address_recording_date,
    CAST(rtt_summary.recording_date as TEXT) as latest_owners_recording_date,
    computed_location,
    1 as grantees_source_priority
    FROM opa_properties_public JOIN (
        SELECT 
        opa_account_num, grantees, recording_date, document_type,
        --reconstruct address from component parts
        CONCAT(
            address_low,
            CASE WHEN address_low_suffix is null THEN '' ELSE address_low_suffix END,
            CASE WHEN address_low_frac is null THEN '' ELSE CONCAT(' ',address_low_frac) END,
            CASE WHEN address_high is null THEN '' ELSE CONCAT('-',address_high) END,
            CASE WHEN street_predir is null THEN '' ELSE CONCAT(' ',street_predir) END,
            CASE WHEN rtt_summary.street_name is null THEN '' ELSE CONCAT(' ',rtt_summary.street_name) END,
            CASE WHEN street_postdir is null THEN '' ELSE CONCAT(' ',street_postdir) END,
            CASE WHEN street_suffix is null THEN '' ELSE CONCAT(' ',street_suffix) END,
            CASE WHEN unit_num is null THEN '' ELSE CONCAT(' UNIT ',unit_num) END
        ) as computed_location
        from rtt_summary 
        where
        (
            (
                cast(address_low as int) >= {address_low}
                AND cast(address_low as int) <= {address_ceil}
            )
            OR (
                cast(address_low as int)>= {address_floor}
                AND cast(address_low as int) <= {address_ceil}
                AND cast(address_high as int) >= {address_remainder}
            )
        )
        AND STREET_NAME LIKE '%{street_name}%'
        {street_dir_str}
        {address_low_suffix_str}
        {unit_str}
        AND opa_account_num is not null
        ORDER by document_id desc LIMIT 1
        ) rtt_summary
    ON rtt_summary.opa_account_num = opa_properties_public.parcel_number
    -- as backup, just get any address where the location matches the search
    UNION ALL
    SELECT distinct location, parcel_number as opa_account_num, concat_ws('; ', owner_1, owner_2) as grantees, 
    mailing_address_1, mailing_address_2, mailing_care_of, 
    CAST(recording_date as TEXT) as mailing_address_recording_date, 
    null as latest_owners_recording_date,
    location as computed_location,
    2 as grantees_source_priority
    FROM opa_properties_public WHERE location like '{search_to_match}%' 
    """
    df = carto_request(query)
    # Sort by similarity of computed location to the search you are looking for
    df["similarity"] = df["computed_location"].apply(
        lambda x: fuzz.ratio(x, search_to_match)
    )
    # if same property shows up in both, take first entry because it has more accurate grantee data
    df.sort_values(
        ["similarity", "grantees_source_priority"], inplace=True, ascending=False
    )
    df = df.groupby("opa_account_num").first().reset_index()

    # temporary
    def aka_location(x):
        if x.location != x.computed_location:
            return x.computed_location + f" (a.k.a. {x.location})"
        else:
            return x.computed_location

    if not df.empty:
        df["location_unit"] = df.apply(aka_location, axis=1)
        df["description"] = df["grantees"]
        df["parcel_number"] = df["opa_account_num"]
    return {
        "success": True,
        "results": df[:n_results].to_dict("records"),
        "query": query,
        "metadata": {"search_to_match": search_to_match, "n_results": n_results},
    }