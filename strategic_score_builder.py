import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load clustered data (GDP, Inflation, FDI, Sentiment)
df = pd.read_csv("clustered_data.csv")

# --- Add manually estimated strategic features ---
manual_data = {
    "country": ["United States", "India", "China"],
    "F500_Score": [10, 7, 6],             # From Statista/estimated
    "DigitalInfra": [1, 1, 1],            # All 3 have robust DPI
    "CulturalOpenness": [4, 3, 2]         # Hofstede + expat data influence
}

manual_df = pd.DataFrame(manual_data)
df = pd.merge(df, manual_df, on="country", how="left")

# --- Normalize selected columns ---
scaler = MinMaxScaler()

# Invert inflation (higher = worse)
df["Inflation_Inverse"] = df["Inflation"].max() - df["Inflation"]

cols_to_normalize = [
    "GDP_per_capita", "Inflation_Inverse", "FDT-percent_GDP",
    "F500_Score", "DigitalInfra", "CulturalOpenness"
]

df_scaled = pd.DataFrame(scaler.fit_transform(df[cols_to_normalize]), columns=[c + "_scaled" for c in cols_to_normalize])
df = pd.concat([df, df_scaled], axis=1)

# --- Weighted score computation ---
weights = {
    "GDP_per_capita_scaled": 0.25,
    "Inflation_Inverse_scaled": 0.15,
    "FDT-percent_GDP_scaled": 0.15,
    "F500_Score_scaled": 0.15,
    "DigitalInfra_scaled": 0.15,
    "CulturalOpenness_scaled": 0.15
}

df["StrategicFitScore"] = sum(df[col] * weight for col, weight in weights.items())
df["StrategicFitScore"] = (df["StrategicFitScore"] * 100).round(2)

# Save
df.to_csv("strategic_scores.csv", index=False)
print("strategic_scores.csv created with Strategic Fit Scores.")
