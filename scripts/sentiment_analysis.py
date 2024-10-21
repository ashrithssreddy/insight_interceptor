
def identify_topics(review_text):
    """Identify topics from the review text using the OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Extract the main topics discussed in the following text: '{review_text}'. List them."}
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

        # Append the topic sentiments in JSON format
        sentiment_results.append(json.dumps(topic_sentiments))

    # Create a new DataFrame to hold sentiment results
    reviews_df['Sentiment JSON'] = sentiment_results  # Add JSON column to DataFrame

    return reviews_df
