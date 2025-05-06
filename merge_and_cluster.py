import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#Load economic data 
econ_df = pd.read_csv("merged_econ_indicators.csv")
econ_df = econ_df.reset_index()

#Use latest year available for each country
latest_econ = econ_df.groupby('country').last().reset_index()

#Load sentiment data
sent_df = pd.read_csv("country_sentiment.csv")

#Merge on country name
merged_df = pd.merge(latest_econ, sent_df, left_on='country', right_on='Country', how='inner')
merged_df = merged_df.drop(columns=['Country'])

print("Merged data:")
print(merged_df.head())

#Normalize & Cluster the data
features = ["GDP_per_capita", "Inflation", "FDT-percent_GDP", "AvgSentiment"]
X = merged_df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42)
merged_df['Cluster'] = kmeans.fit_predict(X_scaled)

#Save the clustered data
merged_df.to_csv("clustered_data.csv", index=False)
print("Clustered data saved to clustered_data.csv")

#Plot the clusters
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X["GDP_per_capita"], X["Inflation"], c=merged_df['Cluster'], cmap='viridis', s=100)
plt.xlabel("GDP per Capita")
plt.ylabel("Inflation Rate(%)")
plt.title("Country Clusters: Economic + Sentiment")
plt.grid(True)
plt.savefig("country_clusters.png")
plt.show()