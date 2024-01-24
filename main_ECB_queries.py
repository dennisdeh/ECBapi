from ECBapi.ECB_queries import ECB_query

# Example 1: HICP - Actual rentals for housing, Monthly Index, Eurostat, Neither seasonally nor working day adjusted
df1 = ECB_query(series="ICP.M.U2.N.041000.4.INX")

# Example 2: ECB reference exchange rate, Canadian dollar/Euro, 2:15 pm (C.E.T.)
df2 = ECB_query(series="EXR.D.CAD.EUR.SP00.A")

# Example 3: Inflation index (Harmonised Index of Consumer Prices (HICP) in Euro area)
df3 = ECB_query(series="ICP.M.U2.N.000000.4.ANR")
