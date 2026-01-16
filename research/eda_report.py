import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# 1. Setup Directories
os.makedirs('docs/plots', exist_ok=True)
os.makedirs('data', exist_ok=True)

def clean_text_simple(text):
    if pd.isna(text): return ""
    text = re.sub(r'\[.*?\]', '', str(text)) # Remove ticket IDs in brackets
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special chars/numbers
    return text.strip().lower()

def run_full_analysis():
    print("📈 Starting EDA and Preprocessing Analysis...")
    
    # Load the advanced dataset
    df = pd.read_csv('data/incidents_advanced.csv')
    
    # --- DATA CLEANING & PREPROCESSING ---
    df['clean_description'] = df['description'].apply(clean_text_simple)
    df['text_len_before'] = df['description'].str.len()
    df['text_len_after'] = df['clean_description'].str.len()

    # --- VISUALIZATION 1: Category Distribution ---
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    ax = sns.countplot(data=df, x='category', hue='priority', palette='magma')
    plt.title('Ticket Volume by Category and Priority', fontsize=15)
    plt.xlabel('Incident Category', fontsize=12)
    plt.ylabel('Number of Tickets', fontsize=12)
    plt.legend(title='Priority', loc='upper right')
    plt.savefig('docs/plots/category_dist.png', dpi=300)
    print("✔️ Saved: docs/plots/category_dist.png")

    # --- VISUALIZATION 2: Resolution Bottlenecks ---
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='priority', y='resolution_time_hrs', palette='viridis', 
                order=['Low', 'Medium', 'High', 'Critical'])
    plt.title('Resolution Latency (MTTR) by Priority Level', fontsize=15)
    plt.xlabel('Priority', fontsize=12)
    plt.ylabel('Hours to Resolve', fontsize=12)
    plt.savefig('docs/plots/resolution_trends.png', dpi=300)
    print("✔️ Saved: docs/plots/resolution_trends.png")

    # --- VISUALIZATION 3: Preprocessing Impact (Histogram) ---
    plt.figure(figsize=(12, 6))
    sns.kdeplot(df['text_len_before'], label='Raw Text', fill=True, color='red')
    sns.kdeplot(df['text_len_after'], label='Cleaned Text', fill=True, color='green')
    plt.title('Text Density: Raw vs. Preprocessed (Tokens)', fontsize=15)
    plt.xlabel('Character Count', fontsize=12)
    plt.legend()
    plt.savefig('docs/plots/preprocessing_impact.png', dpi=300)
    print("✔️ Saved: docs/plots/preprocessing_impact.png")

    # Summary Statistics for the Portfolio
    print("\n📋 DATA INSIGHTS FOR YOUR INTERVIEW:")
    print(f"- Total Tickets Processed: {len(df)}")
    print(f"- Average Resolution Time: {df['resolution_time_hrs'].mean():.2f} hours")
    print(f"- Reduction in Noise (Avg Chars Removed): {df['text_len_before'].mean() - df['text_len_after'].mean():.2f}")

if __name__ == "__main__":
    run_full_analysis()