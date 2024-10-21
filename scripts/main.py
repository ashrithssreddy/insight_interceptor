import pandas as pd
from sentiment_analysis import analyze_sentiment
from topic_categorization import categorize_topic

def main():
    """Entry point for the Insight Interceptor."""
    
    # Load the dataset
    reviews_df = pd.read_csv('docs/play_store_reviews.csv')

    # Create new columns for sentiment and topic
    reviews_df['Sentiment'] = reviews_df['Review Text'].apply(analyze_sentiment)
    reviews_df['Topic'] = reviews_df['Review Text'].apply(categorize_topic)

    # Save the updated dataset
    updated_dataset_path = 'docs/play_store_reviews_categorized.csv'
    reviews_df.to_csv(updated_dataset_path, index=False)

    print(f"Updated dataset saved to {updated_dataset_path}")

if __name__ == "__main__":
    main()
