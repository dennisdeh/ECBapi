"""
This little API can fetch data from the ECB statistics data bank.
It will fetch 1 data column at a time, and return a time-series as
a pd.DataFrame (with date-time as an index).
Small checks are performed.

The only input is the series name, corresponding to the 'Series Key'
of the table that one wants to fetch.
"""
from ECBapi.ECB_queries import ECB_query

# Example 1: HICP - Actual rentals for housing, Monthly Index, Eurostat, Neither seasonally nor working day adjusted
df = ECB_query(series="ICP.M.U2.N.041000.4.INX")

# Example 2: ECB reference exchange rate, Canadian dollar/Euro, 2:15 pm (C.E.T.)
df = ECB_query(series="EXR.D.CAD.EUR.SP00.A")
