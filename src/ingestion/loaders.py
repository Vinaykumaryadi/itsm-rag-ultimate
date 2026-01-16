import re
import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

def clean_incident_text(text):
    if pd.isna(text): return ""
    text = text.lower()
    # Remove ticket metadata like [RE: Ticket #...]
    text = re.sub(r'\[.*?\]', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

def load_preprocessed_incidents():
    df = pd.read_csv('data/incidents_advanced.csv')
    
    # Pre-processing steps
    df['description'] = df['description'].apply(clean_incident_text)
    df['content'] = df['title'] + " " + df['description'] + " Category: " + df['category']
    
    loader = DataFrameLoader(df, page_content_column="content")
    return loader.load()