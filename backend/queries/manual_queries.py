MANUAL_MAILING_ADDRESS_QUERIES = {
    "Odin Properties": """
        SELECT mailing_street, mailing_address_1, mailing_address_2, mailing_care_of, owner_1, owner_2
FROM opa_properties_public
WHERE (
        mailing_street like '1200 CALLOWHILL%' AND mailing_street != '1200 CALLOWHILL ST #302'
    ) OR 
    ( 
      mailing_street like '%1500 MARKET%' and  mailing_address_1 in ('SUITE 3310E','SUITE 331OE')
    )
GROUP by mailing_street, mailing_address_1, mailing_address_2, mailing_care_of, owner_1, owner_2
"""
}
