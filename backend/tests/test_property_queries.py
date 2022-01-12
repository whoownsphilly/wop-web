from backend.queries import (
        property_page_results
)


def test_property_page_results():
    parcel_number = '881547685'
    result = property_page_results(parcel_number)
    import pdb;pdb.set_trace()
