import csv
import tweepy
import re
from textblob import TextBlob
from py2neo import Graph
# Authenticate with Twitter API
consumer_key = "z5Ww3mTPR4YBrZD40q6Kb2TQ4"
consumer_secret = "j55DMW2jkra7ojkQzJBueECsnNGZXKVqhlOJPUSFNmJQ9Gm1o6"
access_token = "848405441851908096-UAaxiujCSi02K2qWYNPNMFwi4AUAeKY"
access_token_secret = "wx6tfVIWsJYfmKae8W2e5YJfu0Yaiwjbt86Ir5HljCwpL"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Define the HP laptop models and HP printer models
laptop_models = ["HP Spectre", "HP Envy", "HP Pavilion"]
printer_models = ["HP LaserJet", "HP OfficeJet", "HP DeskJet"]

# Combine laptop models and printer models with keywords
keywords = ["HP laptops", "HP printers"] + laptop_models + printer_models

# Create a search query using OR operators
query = " OR ".join(keywords)

# Scrape tweets containing the keywords or hashtags
tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(1000)

# Preprocess and extract data from tweets
data = []
for tweet in tweets:
    # Preprocess the tweet text
    text = tweet.text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"\@\w+|\#", "", text)  # Remove @ mentions and hashtags
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation


# Perform sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    sentiment_label = "Unknown"
    if sentiment > 0:
        sentiment_label = "Appreciation"
    elif sentiment < 0:
        sentiment_label = "Complaint"
    else:
        sentiment_label = "Neutral"

    # Extract the specific phrase or word related to sentiment
    phrase = ""
    if sentiment_label != "Neutral":
        phrase = str(blob.sentences[0])

    # Extract the complaint or feature mentioned in the tweet
    complaint = ""
    feature = ""
    if sentiment_label == "Complaint":
        complaint_keywords = ["problem", "issue", "error", "fault"]
        for keyword in complaint_keywords:
            if keyword in text:
                complaint = keyword
                match = re.search(rf"\b{keyword}\b(.+)", text)
                if match:
                    feature = match.group(1).strip()
                break

    # Tag the tweet with the respective HP product model
    tagged_model = ""
    for model in laptop_models + printer_models:
        if model.lower() in text:
            tagged_model = model
            break

    # Store the tweet data in a dictionary
    tweet_data = {
        "Tweet": tweet.text,
        "TweetLink": f'https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}',
        "user": tweet.user.screen_name,
        "Date": tweet.created_at.date(),
        "Month": tweet.created_at.strftime("%B"),
        "sentiment": sentiment_label,

        "model": tagged_model
    }
    data.append(tweet_data)

# Save the data to a CSV file
csv_filename = "twitter_data.csv"
csv_fields = ["Tweet", "TweetLink", "user", "Date", "Month", "sentiment","model"]

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_fields)
    writer.writeheader()
    for tweet_data in data:
        writer.writerow(tweet_data)

print("Data saved to", csv_filename)
