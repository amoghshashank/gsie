import wbdata
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Define countries by ISO codes
countries = ["IND", "USA", "CHN"]

# GDP per capita (constant 2015 US$)
indicators = {"NY.GDP.PCAP.KD": "GDP_per_capita"}

# Time period
data_date = datetime.datetime(2010, 1, 1)

# Fetch full dataset
df = wbdata.get_dataframe(indicators, country=countries)

# Reset index and filter years manually (e.g., 2010–2022)
df = df.reset_index()
df['year'] = pd.DatetimeIndex(df['date']).year
df = df[(df['year'] >= 2010) & (df['year'] <= 2022)]


# Pivot table: years as rows, countries as columns
df_pivot = df.pivot(index="date", columns="country", values="GDP_per_capita")
print(df_pivot.tail(10))  # ← check last 10 rows

# Force plot of full range by dropping rows with too many NaNs
df_pivot = df_pivot.dropna(how='all')  # keep rows with at least one value


# Plot
df_pivot.plot(title="GDP per Capita (2010–2022)", figsize=(10, 6))
plt.ylabel("USD")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig("gdp_plot.png")
plt.show()
