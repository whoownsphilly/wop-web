from backend.queries import property_page_results


def test_property_page_results():
    # parcel_number = '881547685'
    parcel_number = "881028600"
    result = property_page_results(parcel_number)
    assert result
