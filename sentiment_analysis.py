import pandas as pd
import openai
import yaml
import json

# Load API keys from the config file
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

openai.api_key = config['openai']['api_key']

def identify_topics(review_text):
    """Identify topics from the review text using the OpenAI API."""
    try:
        prompt = (
            f"From the following review, identify concise key topics (1-2 words) discussed: \"{review_text}\". "
            "Provide a list of distinct topics separated by commas without any additional text or formatting."
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=100
        )
        
        content = response['choices'][0]['message']['content'].strip()
        
        # Remove any surrounding markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1].strip()
        
        # Split the topics by comma and strip whitespace and quotes
        topics = [topic.strip().strip('"') for topic in content.split(',') if topic.strip()]
        
        return topics
    
    except Exception as e:
        print(f"Error identifying topics in review: {review_text}\nError: {e}")
        return []

def compute_overall_sentiment(topic_sentiments):
    """Compute overall sentiment based on individual topic sentiments."""
    sentiment_scores = {"Positive": 1, "Neutral": 0, "Negative": -1}
    total = sum(sentiment_scores.get(ts['sentiment'], 0) for ts in topic_sentiments)
    
    if total > 0:
        return "Positive"
    elif total < 0:
        return "Negative"
    else:
        return "Neutral"

def determine_sentiment(reviews_df):
    """Determine the sentiment scores for each topic in the DataFrame using the OpenAI API."""
    sentiment_results = []

    for review_text in reviews_df['Review Text']:
        identified_topics = identify_topics(review_text)
        topics_sentiments = []
        
        for topic in identified_topics:
            try:
                prompt = (
                    f"Determine the sentiment for the topic '{topic}' in the following text: \"{review_text}\". "
                    "Respond with a sentiment score of Positive, Negative, or Neutral without any additional text or formatting."
                )
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=10
                )
                
                sentiment = response['choices'][0]['message']['content'].strip()
                
                if sentiment not in ["Positive", "Negative", "Neutral"]:
                    sentiment = "Neutral"
                
                topics_sentiments.append({
                    "topic": topic,
                    "sentiment": sentiment
                })
        
            except Exception as e:
                print(f"Error determining sentiment for topic '{topic}' in review: {review_text}\nError: {e}")
                topics_sentiments.append({
                    "topic": topic,
                    "sentiment": "Neutral"
                })
        
        overall_sentiment = compute_overall_sentiment(topics_sentiments)
        
        sentiment_results.append({
            "topics_sentiments": topics_sentiments,
            "overall_sentiment": overall_sentiment
        })

    sentiment_df = pd.DataFrame(sentiment_results)
    reviews_df = pd.concat([reviews_df.reset_index(drop=True), sentiment_df], axis=1)

    return reviews_df

# Example usage
if __name__ == "__main__":
    # Load your reviews data into a DataFrame
    reviews_df = pd.read_csv('data/reviews.csv')

    # Perform sentiment analysis
    enriched_reviews_df = determine_sentiment(reviews_df)

    # Save the enriched DataFrame to a new CSV
    enriched_reviews_df.to_csv('data/reviews_with_sentiment.csv', index=False)

    # Save to JSON for better structure preservation
    enriched_reviews_df.to_json('data/reviews_with_sentiment.json', orient='records', lines=True)
