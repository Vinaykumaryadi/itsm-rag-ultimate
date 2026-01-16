import re
import pandas as pd

def clean_text(text):
    """Standardizes text for better embedding quality."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()    # Remove extra whitespace
    return text

def preprocess_incidents(file_path):
    df = pd.read_csv(file_path)
    # Feature Engineering: Combine Title and Description for better context
    df['combined_text'] = df['title'] + " " + df['description']
    df['combined_text'] = df['combined_text'].apply(clean_text)
    
    # Filter out tickets that are too short to be useful
    df = df[df['combined_text'].str.len() > 10]
    
    return df