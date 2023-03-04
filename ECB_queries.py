from urllib.request import urlopen
from xmltodict import parse
import pandas as pd


def ECB_query(series: str) -> pd.DataFrame:
    """
    Fetches the newest data available for a given statistical series (one data
    column only) and returns a data frame.

    Parameters
    ---------
    series: str
        Name of the table. Of the format "CATEGORY/TABLE".

    Returns
    -------
    pd.DataFrame:
        DataFrame with date column and value of the series.
    """
    # step 1: replace first "." with "/" if needed
    if series.find("/") == -1:  # check if a "/" exists
        series = series.replace(".", "/", 1)  # replace just once
    else:
        pass

    # step 2: open data and parse
    with urlopen(f"https://sdw-wsrest.ecb.europa.eu/service/data/{series}") as url:
        raw = parse(url.read().decode('utf8'))
    data = raw['message:GenericData']['message:DataSet']['generic:Series']['generic:Obs']

    res_val = {x['generic:ObsDimension']['@value']:
                   float(x['generic:ObsValue']['@value'])
               for x in data}

    df = pd.DataFrame(res_val.items(), columns=['date', 'value'])
    df["date"] = pd.to_datetime(df["date"])

    return df.set_index("date")
