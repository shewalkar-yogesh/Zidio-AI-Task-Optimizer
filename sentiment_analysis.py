from textblob import TextBlob
import re

def clean_text(text):
    """
    Clean the input text by removing special characters, extra spaces, etc.
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def analyze_sentiment(text):
    """
    Analyze the sentiment of the provided text using TextBlob with enhanced processing.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        tuple: (sentiment_score, polarity)
    """
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Create TextBlob object
    analysis = TextBlob(cleaned_text)
    
    # Get sentiment polarity (-1 to 1) and subjectivity (0 to 1)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity
    
    # Apply weighting to polarity based on subjectivity
    # More subjective text can express stronger sentiment
    weighted_polarity = polarity * (0.5 + 0.5 * subjectivity)
    
    # Normalize the score to range from 0 to 1 for easier visualization
    normalized_score = (weighted_polarity + 1) / 2
    
    # Return the normalized score and original polarity
    return normalized_score, polarity

def get_emotion_detail(text):
    """
    Extract emotional details from text using TextBlob's noun phrases.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        list: Key emotional phrases detected
    """
    analysis = TextBlob(text)
    
    # Get noun phrases which may contain emotional context
    phrases = analysis.noun_phrases
    
    # Filter phrases to those that might indicate emotion (limited capability)
    emotion_indicators = []
    if phrases:
        # Return up to 3 phrases
        return list(phrases)[:3]
    
    return emotion_indicators

def get_emotion_label(sentiment_score):
    """
    Convert a sentiment score to an emotion label with finer-grained emotions.
    
    Args:
        sentiment_score (float): Normalized sentiment score (0-1)
        
    Returns:
        str: Emotion label (Negative, Neutral, Positive)
    """
    # Convert normalized score back to the -1 to 1 range
    polarity = sentiment_score * 2 - 1
    
    # More fine-grained emotion labeling
    if polarity <= -0.6:
        return "Negative"  # Very negative
    elif polarity < -0.2:
        return "Negative"  # Somewhat negative
    elif polarity <= 0.2:
        return "Neutral"   # Neutral
    elif polarity < 0.6:
        return "Positive"  # Somewhat positive
    else:
        return "Positive"  # Very positive
