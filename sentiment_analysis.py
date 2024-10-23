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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "user", "content": f"Extract the main topics discussed in the following text: '{review_text}'. List them."}
                # {"role": "user", "content": f"From the following review, identify specific features or aspects discussed and list them as separate topics: '{review_text}'. Please format your response as a JSON object with each topic as a key."}
                {"role": "user", "content": f"From the following review, identify concise key topics (1-2 words) discussed: '{review_text}'. Provide a list of distinct topics."}


            ]
        )
        
        topics = response['choices'][0]['message']['content'].strip().split(', ')
        return topics  # Return a list of identified topics

    except Exception as e:
        print(f"Error identifying topics in review: {review_text}\nError: {e}")
        return []

def determine_sentiment(reviews_df):
    """Determine the sentiment scores for each topic in the DataFrame using the OpenAI API."""
    sentiment_results = []

    for review_text in reviews_df['Review Text']:
        identified_topics = identify_topics(review_text)
        topic_sentiments = {}
        
        # Overall sentiment variable
        overall_sentiment = None

        for topic in identified_topics:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"Determine the sentiment for the topic '{topic}' in the following text: '{review_text}'. Respond with a sentiment score of Positive, Negative, or Neutral."}
                    ]
                )
                
                sentiment = response['choices'][0]['message']['content'].strip()
                topic_sentiments[topic] = sentiment

            except Exception as e:
                print(f"Error determining sentiment for topic '{topic}' in review: {review_text}\nError: {e}")
                topic_sentiments[topic] = None  # Append None in case of error

        # Calculate overall sentiment (you can define how to derive this)
        overall_sentiment = "Neutral"  # Placeholder for overall sentiment calculation logic

        # Append structured result
        sentiment_results.append({
            "topics": topic_sentiments,
            "overall_sentiment": overall_sentiment
        })

    # Create a new DataFrame to hold sentiment results
    sentiment_df = pd.DataFrame(sentiment_results)
    reviews_df = pd.concat([reviews_df, sentiment_df], axis=1)  # Combine original DataFrame with sentiments

    return reviews_df
