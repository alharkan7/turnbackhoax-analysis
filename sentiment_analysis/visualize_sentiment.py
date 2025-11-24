import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_sentiment_distribution(summary_file, output_image, title, entity_col='Entity'):
    """Visualizes the sentiment distribution for each entity."""
    print(f"Reading summary data from {summary_file}...")
    try:
        df = pd.read_csv(summary_file)
    except Exception as e:
        print(f"Error reading summary file: {e}")
        return

    # Check if entity_col exists, if not try 'Candidate'
    if entity_col not in df.columns:
        if 'Candidate' in df.columns:
            entity_col = 'Candidate'
        else:
            print(f"Error: Column '{entity_col}' not found in {summary_file}. Columns: {df.columns}")
            return

    # Melt the DataFrame for plotting (optional, but good for seaborn)
    # But here we use pandas plot which expects wide format for stacked bars
    
    # Set plot style
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # Create stacked bar chart
    # We use a custom color palette
    colors = {"Positive (%)": "#2ecc71", "Neutral (%)": "#95a5a6", "Negative (%)": "#e74c3c"}
    
    # Plotting
    df_plot = df.set_index(entity_col)[['Positive (%)', 'Neutral (%)', 'Negative (%)']]
    ax = df_plot.plot(kind='bar', stacked=True, color=[colors['Positive (%)'], colors['Neutral (%)'], colors['Negative (%)']], figsize=(12, 8))

    plt.title(title, fontsize=16)
    plt.xlabel(entity_col, fontsize=14)
    plt.ylabel('Percentage (%)', fontsize=14)
    plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
    plt.legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add percentage labels on the bars
    for c in ax.containers:
        # Only label if the bar height is significant enough to hold text
        labels = [f'{v.get_height():.1f}%' if v.get_height() > 5 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', color='white', fontsize=9, weight='bold')

    plt.tight_layout()
    
    print(f"Saving visualization to {output_image}...")
    plt.savefig(output_image, dpi=300)
    print("Done.")

def main():
    # Politics
    if os.path.exists("candidate_sentiment_summary.csv"):
        visualize_sentiment_distribution(
            "candidate_sentiment_summary.csv", 
            "candidate_sentiment_distribution.png", 
            "Sentiment Distribution by Political Candidate",
            entity_col="Candidate"
        )

    # Scam
    if os.path.exists("scam_sentiment_summary.csv"):
        visualize_sentiment_distribution(
            "scam_sentiment_summary.csv", 
            "scam_sentiment_distribution.png", 
            "Sentiment Distribution by Scam Entity/Keyword",
            entity_col="Entity"
        )

    # Others
    if os.path.exists("others_sentiment_summary.csv"):
        visualize_sentiment_distribution(
            "others_sentiment_summary.csv", 
            "others_sentiment_distribution.png", 
            "Sentiment Distribution by Topic (Others Category)",
            entity_col="Entity"
        )

if __name__ == "__main__":
    main()
