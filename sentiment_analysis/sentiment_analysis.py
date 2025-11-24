import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import re
import os

def load_data(filepath):
    """Loads the CSV data."""
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def load_model():
    """Loads the pre-trained sentiment analysis model."""
    print("Loading sentiment analysis model...")
    # Using a popular Indonesian sentiment analysis model
    model_name = "w11wo/indonesian-roberta-base-sentiment-classifier"
    try:
        sentiment_classifier = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
        print("Model loaded successfully.")
        return sentiment_classifier
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def identify_entities(text, entities):
    """Identifies which entities are mentioned in the text."""
    mentioned = []
    if not isinstance(text, str):
        return mentioned
    
    text_lower = text.lower()
    for entity, keywords in entities.items():
        for keyword in keywords:
            if keyword in text_lower:
                mentioned.append(entity)
                break # Count entity once per text
    return mentioned

def analyze_sentiment(df, classifier, entities):
    """Performs sentiment analysis and entity detection."""
    print("Analyzing sentiment and identifying entities...")
    
    results = []
    
    for index, row in tqdm(df.iterrows(), total=len(df)):
        text = row['HOAX_TEXT']
        
        # Skip if text is not a string
        if not isinstance(text, str):
            continue
            
        # Truncate text to fit model's max length (usually 512 tokens)
        truncated_text = text[:512] 
        
        try:
            # Predict sentiment
            prediction = classifier(truncated_text)[0]
            sentiment_label = prediction['label']
            sentiment_score = prediction['score']
            
            # Identify entities
            mentioned_entities = identify_entities(text, entities)
            
            results.append({
                'ID': row['ID'],
                'TITLE': row['TITLE'],
                'HOAX_TEXT': text,
                'SENTIMENT_LABEL': sentiment_label,
                'SENTIMENT_SCORE': sentiment_score,
                'ENTITIES_MENTIONED': ", ".join(mentioned_entities)
            })
            
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            continue
            
    return pd.DataFrame(results)

def aggregate_results(df, entities):
    """Aggregates sentiment results by entity."""
    print("Aggregating results...")
    
    summary_data = []
    
    for entity in entities.keys():
        # Filter rows where the entity is mentioned
        entity_df = df[df['ENTITIES_MENTIONED'].apply(lambda x: entity in x.split(", "))]
        
        total_mentions = len(entity_df)
        
        if total_mentions > 0:
            sentiment_counts = entity_df['SENTIMENT_LABEL'].value_counts(normalize=True) * 100
            
            summary_data.append({
                'Entity': entity,
                'Total Mentions': total_mentions,
                'Positive (%)': sentiment_counts.get('positive', 0),
                'Negative (%)': sentiment_counts.get('negative', 0),
                'Neutral (%)': sentiment_counts.get('neutral', 0)
            })
        else:
             summary_data.append({
                'Entity': entity,
                'Total Mentions': 0,
                'Positive (%)': 0,
                'Negative (%)': 0,
                'Neutral (%)': 0
            })
            
    return pd.DataFrame(summary_data)

def run_analysis(input_file, output_results_file, output_summary_file, entities, classifier):
    """Runs the full analysis pipeline for a specific configuration."""
    print(f"--- Starting analysis for {input_file} ---")
    
    # Load data
    df = load_data(input_file)
    if df is None:
        return

    # Analyze
    results_df = analyze_sentiment(df, classifier, entities)
    
    # Save detailed results
    print(f"Saving detailed results to {output_results_file}...")
    results_df.to_csv(output_results_file, index=False)
    
    # Aggregate
    summary_df = aggregate_results(results_df, entities)
    
    # Save summary
    print(f"Saving summary to {output_summary_file}...")
    summary_df.to_csv(output_summary_file, index=False)
    
    print(f"Analysis completed for {input_file}.")
    print(summary_df)
    print("-" * 30)

def main():
    # Load model once
    classifier = load_model()
    if classifier is None:
        return

    # --- Politics Configuration (Already done, but kept for reference/re-run if needed) ---
    # politics_config = {
    #     "input_file": "../topic_modeling/politics_hoax_text.csv",
    #     "output_results": "politics_sentiment_results.csv",
    #     "output_summary": "politics_sentiment_summary.csv",
    #     "entities": {
    #         "Prabowo": ["prabowo", "bowo", "02", "gemoy"],
    #         "Gibran": ["gibran", "samsul", "02"],
    #         "Anies": ["anies", "baswedan", "amin", "01"],
    #         "Ganjar": ["ganjar", "pranowo", "03"],
    #         "Jokowi": ["jokowi", "joko widodo", "presiden", "mulyono"]
    #     }
    # }
    # run_analysis(politics_config["input_file"], politics_config["output_results"], politics_config["output_summary"], politics_config["entities"], classifier)

    # --- Scam Configuration ---
    scam_config = {
        "input_file": "../topic_modeling/scam_category/scam_hoax_text.csv",
        "output_results": "scam_sentiment_results.csv",
        "output_summary": "scam_sentiment_summary.csv",
        "entities": {
            "Bank BNI": ["bni", "bank negara indonesia"],
            "Bank BRI": ["bri", "bank rakyat indonesia"],
            "Bank Indonesia": ["bank indonesia", "bi"],
            "Raffi Ahmad": ["raffi", "ahmad", "rans"],
            "Baim Wong": ["baim", "wong", "bapau"],
            "Najwa Shihab": ["najwa", "shihab", "nana"],
            "Pertamina": ["pertamina"],
            "OJK": ["ojk", "otoritas jasa keuangan"],
            "Giveaway": ["giveaway", "bagi-bagi", "hadiah"],
            "Lowongan Kerja": ["loker", "lowongan", "rekrutmen"],
            "Pinjol": ["pinjol", "pinjaman online", "dana kaget"]
        }
    }
    run_analysis(scam_config["input_file"], scam_config["output_results"], scam_config["output_summary"], scam_config["entities"], classifier)

    # --- Others Configuration ---
    others_config = {
        "input_file": "../topic_modeling/others_category/others_hoax_text.csv",
        "output_results": "others_sentiment_results.csv",
        "output_summary": "others_sentiment_summary.csv",
        "entities": {
            "Bencana Alam": ["gempa", "tsunami", "banjir", "longsor", "angin", "puting beliung"],
            "Kesehatan": ["vaksin", "covid", "virus", "pneumonia", "obat", "dokter"],
            "Konflik Internasional": ["israel", "palestina", "gaza", "hamas", "rohingya", "ukraina", "rusia"],
            "Sepak Bola": ["piala asia", "timnas", "fifa", "afc", "bola"]
        }
    }
    run_analysis(others_config["input_file"], others_config["output_results"], others_config["output_summary"], others_config["entities"], classifier)

if __name__ == "__main__":
    main()
