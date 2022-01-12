SELECT mailing_street, mailing_address_1, mailing_address_2, owner_1, owner_2, mailing_care_of
FROM opa_properties_public
WHERE mailing_street like '1845 WALNUT ST%'
AND (mailing_address_1 like '%2000' or mailing_address_1 like '%2200')
GROUP BY mailing_street, mailing_address_1, mailing_address_2 , mailing_care_of, owner_1, owner_2
