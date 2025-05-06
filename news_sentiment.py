import requests
from textblob import TextBlob
import pandas as pd
import time

# Countries and queries
country_queries = {
    "India": "India politics",
    "United States": "United States politics",
    "China": "China politics"
}

api_key = "111c5b54f8924a0491423c6775e1270e"  # Replace with your key
sentiment_summary = []

for country, query in country_queries.items():
    url = (
        f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=10&apiKey={api_key}"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])
    
    sentiments = []
    for article in articles:
        text = article["title"] + ". " + (article.get("description") or "")
        sentiment = TextBlob(text).sentiment.polarity
        sentiments.append(sentiment)
    
    avg_sentiment = round(sum(sentiments) / len(sentiments), 3) if sentiments else 0
    sentiment_summary.append({"Country": country, "AvgSentiment": avg_sentiment})
    
    time.sleep(1)  # Respect API rate limits

# Save to CSV
df = pd.DataFrame(sentiment_summary)
df.to_csv("country_sentiment.csv", index=False)
print("Sentiment saved to country_sentiment.csv")
