import numpy as np
import os
import pandas as pd
import requests


DEEDS_WHERE_CLAUSE = """
    document_type='DEED' OR
    document_type='DEED SHERIFF' OR
    document_type='DEED OF CONDEMNATION' OR
    document_type='DEED LAND BANK'
"""


def carto_request(query, as_df=True):
    try:
        response = requests.get("https://phl.carto.com/api/v2/sql", params={"q": query})
        df_json = response.json()
    except:
        raise ValueError(response.text)
    if "rows" not in df_json:
        raise ValueError(f"{query}\n\n{df_json}")
    data = df_json["rows"]
    if as_df:
        return pd.DataFrame(df_json["rows"], columns=list(df_json["fields"].keys()))
    return data


def airtable_request(mailing_street, mailing_address_1):
    airtable_url = os.environ.get("BIOS_URL")
    invisible_fields = ["last_modified_by", "researcher"]
    params = {
        "filterByFormula": 'IF(AND({mailing_street}="'
        + mailing_street
        + '",'
        + '{mailing_address_1}="'
        + mailing_address_1
        + '",'
        + "{show_on_website}=TRUE()),"
        + "TRUE(), FALSE())",
        #'fields': [],
    }
    response = requests.get(airtable_url, params=params)
    if "records" in response.json():
        output_response = {}
        output_response["results"] = []
        records = response.json()["records"]
        output_response["n_results"] = len(records)
        # TODO (clean this up so there is only maybe one entry per mailing address?
        for record in records:
            outputs = {
                key: val
                for key, val in record["fields"].items()
                if key not in invisible_fields
            }
            output_response["results"].append(outputs)
        if records:
            single_record = output_response["results"][0]
            output["owner_by_mailing_address"] = {
                "name": single_record["name_of_possible_owner"],
                "url": single_record["link_to_owner_website"],
            }
            return output
