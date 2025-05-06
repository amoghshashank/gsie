import pandas as pd
from openai import OpenAI
import time

# Initialize OpenAI client (uses your OPENAI_API_KEY env variable)
client = OpenAI()

# Load your scored dataset
df = pd.read_csv("strategic_scores.csv")

# Build prompt function
def generate_prompt(row):
    return f"""
You are a global strategy advisor for international expansion.

Using the CAGE framework (Cultural, Administrative, Geographic, Economic), generate a 2-line strategic summary based on these values:

Country: {row['country']}
GDP per capita: ${round(row['GDP_per_capita'], 2)}
Inflation: {round(row['Inflation'], 2)}%
FDI (% of GDP): {round(row['FDT-percent_GDP'], 2)}
Fortune 500 Score (0–10): {row['F500_Score']}
Digital Infrastructure (1=yes): {row['DigitalInfra']}
Cultural Openness (1–5): {row['CulturalOpenness']}
Strategic Fit Score: {row['StrategicFitScore']}
Political Sentiment: {round(row['AvgSentiment'], 2)}

Be balanced. Highlight strengths, but do not shy away from weaknesses or exceptions (e.g. India's pharma patent flexibility, or China's restrictions).
"""

# Generate insights
summaries = []

for _, row in df.iterrows():
    prompt = generate_prompt(row)
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        summaries.append(summary)
        time.sleep(1)  # Rate limit buffer
    except Exception as e:
        summaries.append(f"Error: {str(e)}")

# Add to DataFrame
df["StrategicInsight"] = summaries

# Save final file
df.to_csv("final_strategic_dataset.csv", index=False)
print("final_strategic_dataset.csv created with AI-powered CAGE summaries.")
