import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("final_strategic_dataset.csv")

# Page config
st.set_page_config(page_title="Global Strategy Intelligence Engine", layout="centered")
st.title("🌍 Global Strategy Intelligence Engine (GSIE)")
st.markdown("Powered by AI + Real Data")

# Sidebar filter
min_score = st.sidebar.slider("Minimum Strategic Fit Score", 0, 100, 50)

filtered_df = df[df["StrategicFitScore"] >= min_score]

# Display top-level summary
st.metric(label="Countries Above Threshold", value=len(filtered_df))

# Loop through countries
for _, row in filtered_df.iterrows():
    with st.expander(f"📌 {row['country']} — Score: {row['StrategicFitScore']}"):
        st.write(row["StrategicInsight"])
        st.write("**Key Metrics:**")
        st.markdown(f"""
        - GDP per capita: ${round(row['GDP_per_capita'], 2)}
        - Inflation: {round(row['Inflation'], 2)}%
        - FDI (% GDP): {round(row['FDT-percent_GDP'], 2)}
        - Fortune 500 Score: {row['F500_Score']}
        - Digital Infra: {"✅ Yes" if row['DigitalInfra'] == 1 else "❌ No"}
        - Cultural Openness: {row['CulturalOpenness']}/5
        """)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Amogh | MVP version. Contact for collaboration or data licensing.")
