import pandas as pd
from sentiment_analysis import determine_sentiment

#def main():
    
"""Entry point for the Insight Interceptor."""

# Load the dataset
reviews_df = pd.read_csv('docs/play_store_reviews.csv').head()

# Determine sentiment using the updated function
reviews_df = determine_sentiment(reviews_df)

# Save the updated dataset
updated_dataset_path = 'docs/play_store_reviews_categorized.csv'
reviews_df.to_csv(updated_dataset_path, index=False)
print(reviews_df)

print(f"Updated dataset saved to {updated_dataset_path}")

#if __name__ == "__main__":
#    main()
