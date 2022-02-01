import numpy as np
import os
import pandas as pd
import httpx


DEEDS_WHERE_CLAUSE = """
    document_type='DEED' OR
    document_type='DEED SHERIFF' OR
    document_type='DEED OF CONDEMNATION' OR
    document_type='DEED LAND BANK'
"""


async def make_async_get_request(url, /, *, params=None):
    async with httpx.AsyncClient() as client:
        return await client.get(url, params=params, follow_redirects=True, timeout=None)


async def carto_request(query, as_df=True):
    response = await make_async_get_request(
        "https://phl.carto.com/api/v2/sql",
        params={"q": query},
    )
    try:
        df_json = response.json()
    except:
        raise ValueError(response.text)
    if "rows" not in df_json:
        raise ValueError(f"{query}\n\n{df_json}")
    data = df_json["rows"]
    if as_df:
        return pd.DataFrame(df_json["rows"], columns=list(df_json["fields"].keys()))
    return data
