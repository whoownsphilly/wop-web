from backend.queries import (
    properties_by_mailing_address_results,
    properties_by_property_autocomplete_results,
    properties_by_owner_name_results,
)


async def test_properties_by_mailing_address_results():
    """
    Test number found through:
    '''
    SELECT r.grantees, r.recording_date, r.opa_account_num, opa.mailing_st
      opa.owner_1, opa.owner_2, opa.recording_date as opa_date
      FROM rtt_summary r JOIN opa_properties_public opa
      on r.opa_account_num = opa.parcel_number
      WHERE  (document_type='DEED' OR
     document_type='DEED SHERIFF' OR
     document_type='DEED OF CONDEMNATION' OR
     document_type='DEED LAND BANK')
     AND r.recording_date != opa.recording_date
     AND mailing_street is not null
     AND grantees like '%LLC%'
     order by r.recording_date desc
      LIMIT 10
    '''
    """
    parcel_number = "032022200"
    result = await properties_by_mailing_address_results(parcel_number)
    assert result

    parcel_number = "881074500"  # a known property with many connected properties
    result = await properties_by_mailing_address_results(parcel_number)
    assert result

    parcel_number = (
        "871540050"  # opa_properties_public.recording_date='2019-07-26T00:00:00Z'
    )
    result = await properties_by_mailing_address_results(parcel_number)
    assert result


async def test_autocomplete():
    properties_to_test = [
        {"address_str": "135 S 23rd Street", "top_result": "881028600"},
        {"address_str": "614 South washington square 912", "top_result": "888050735"},
        {"address_str": "20 S 16TH ST", "top_result": "883422300"},
        {"address_str": "135 S 23rd Street", "top_result": "881028600"},
        {"address_str": "4604 Whitaker Ave", "top_result": "871564840"},
        {"address_str": "4604R Whitaker Ave", "top_result": "421554300"},
    ]
    for test_property in properties_to_test:
        results = await properties_by_property_autocomplete_results(
            test_property["address_str"], n_results=1
        )
        assert results["results"][0]["opa_account_num"] == test_property["top_result"]

    # test that this property returns a null mailing address since owner shouldnt match
    test_property_str = "2542 W OXFORD ST"
    """
    This needs to be implemented on the actual website.
    Right now this does not figure out who the most recent owner is for a given address
    So results of this query would only have the address and the mailing address
    but that is a TODO. IT would involve a bit of a more complex query to get the
    most recent DEED info but I believe that query is already elsewhere.
    """


async def test_properties_by_owner_name_results():
    # results = properties_by_owner_name_results('14 WA PARTNERS LP')
    parcel_number = "032022200"
    # parcel_number = '291284800'
    parcel_number = "032209600"  # odin
    parcel_number = "888060252"  # domb with NaT start_date
    parcel_number = "881074500"  # property timeline misses latest entry
    parcel_number = "871288650"  # domb
    # parcel_number = "881137200"  # broken
    parcel_number = "011156500"  # doesnt return any properties
    results = await properties_by_owner_name_results(parcel_number)
    # This is pretty good, just needs to get synced into the front-end
    assert results
