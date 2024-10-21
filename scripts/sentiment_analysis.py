def analyze_sentiment(review_text):
    """Analyze the sentiment of a review."""
    positive_words = ['great', 'love', 'excellent', 'fantastic', 'amazing']
    negative_words = ['bad', 'hate', 'terrible', 'awful', 'disappointed']

    review_text = review_text.lower()
    positive_score = sum(word in review_text for word in positive_words)
    negative_score = sum(word in review_text for word in negative_words)

    if positive_score > negative_score:
        return 'Positive'
    elif negative_score > positive_score:
        return 'Negative'
    else:
        return 'Neutral'
