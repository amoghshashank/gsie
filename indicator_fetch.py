import wbdata
import pandas as pd
import datetime

#Target countries
countries = ["IND", "USA", "CHN"]

#Economic indicators
indicators = {
    "NY.GDP.PCAP.CD": "GDP_per_capita",     # GDP per capita (current US$)
    "FP.CPI.TOTL.ZG": "Inflation",      # Inflation, consumer prices (annual %)
    "BX.KLT.DINV.CD.WD": "FDT-percent_GDP"       # Foreign direct investment, net inflows (% of GDP)
}   

#Fetch data(no date filtered here due to wbdata version)
df = wbdata.get_dataframe(indicators, country=countries)
df = df.reset_index()

#Filter to relevant years
df["year"] = pd.DatetimeIndex(df["date"]).year
df = df[(df["year"] >= 2010) & (df["year"] <= 2022)]

#Pivot by date + country
df_pivot = df.pivot_table(index=["date", "country"], values=list(indicators.values()))
df_pivot = df_pivot.sort_index()

#Export to CSV
df_pivot.to_csv("merged_econ_indicators.csv")
print("Economic indicators saved to merged_econ_indicators.csv")