This little API can fetch data from the ECB statistical data warehouse.
It will fetch 1 data column at a time, and return a time-series as a pd.DataFrame (with date-time as an index).
Small checks are performed.

The only input is the series name, corresponding to the 'Series Key' of the table that one wants to fetch.
