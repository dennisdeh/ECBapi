from urllib.request import urlopen
from xmltodict import parse
import pandas as pd
import time
from urllib.error import URLError
from http.client import RemoteDisconnected


def ECB_query(series: str,
              retries: int = 3,
              silent: bool = False):
    """
    Fetches the newest data available for a given statistical series (one data
    column only) and returns a data frame.

    Parameters
    ---------
    series: str
        Name of the table. Of the format "CATEGORY/TABLE".
    retries: int
        Number of times to try downloading again
    silent: bool
        Print informative messages?

    Returns
    -------
    pd.DataFrame:
        DataFrame with date column and value of the series.
    """
    # step 0: initialise
    # set some internal parameters
    wait_time_retry = 10
    wait_time_query = 0.1
    # print messages
    if not silent:
        print("Querying data from ECB... ", end="")

    # step 1: replace first "." with "/" if needed
    if series.find("/") == -1:  # check if a "/" exists
        series = series.replace(".", "/", 1)  # replace just once
    else:
        pass

    # step 2: define function that retrieves data and parses
    def get_data(s):
        with urlopen(f"https://data-api.ecb.europa.eu/service/data/{s}") as url:
            raw = parse(url.read().decode('utf8'))
        d = raw['message:GenericData']['message:DataSet']['generic:Series']['generic:Obs']
        return d

    # step 3: open data and parse
    # step 3.1: try to download the data (a couple of times)
    n = 0
    while n < retries:
        try:
            time.sleep(wait_time_query)
            data = get_data(series)
            break  # if succeeded, break the loop
        except URLError or pd.errors.ParserError or RemoteDisconnected:
            if not silent:
                print("Trying downloading again... ", end="")
            n += 1
            data = []
            time.sleep(wait_time_retry)
    # step 3.2: assertions
    if n >= retries:  # raise exception if no data was found
        raise ConnectionError("Could not establish connection to the server or data series was not found")
    if not silent:
        print("Success!")

    # step 4: create data frame in a good format
    res_val = {x['generic:ObsDimension']['@value']: float(x['generic:ObsValue']['@value']) for x in data}
    df = pd.DataFrame(res_val.items(), columns=['date', 'value'])
    # parse dates
    try:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    except ValueError:
        try:
            df["date"] = pd.to_datetime(df["date"], format="mixed")
        except ValueError:
            df["date"] = pd.PeriodIndex(df["date"], freq='Q').to_timestamp()

    return df.set_index("date")
