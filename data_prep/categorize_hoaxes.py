import os
import time
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import json
import typing_extensions as typing

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

# Configuration
INPUT_FILE = "Scraping turnbackhoax.id - Complete.csv"
OUTPUT_FILE = "categorized_hoaxes.csv"
BATCH_SIZE = 50
# Note: User explicitly requested gemini-2.5-flash.
MODEL_NAME = "gemini-2.5-flash" 

def categorize_batch(items):
    # items is a list of dicts: [{'ID': 123, 'TITLE': '...'}, ...]
    
    prompt = """
    You are an expert at categorizing news and claims.
    The data is from turnbackhoax.id, an Indonesian anti-hoax database by MAFINDO.
    
    Categorize each of the following items based on their Title into one of these categories:
    - politics
    - scam
    - others
    
    Return the result as a JSON list of objects, where each object has 'id' and 'category'.
    """
    
    # Prepare the input text
    items_text = ""
    for item in items:
        items_text += f"ID: {item['ID']}\nTitle: {item['TITLE']}\n---\n"
        
    full_prompt = prompt + "\nItems to categorize:\n" + items_text

    # Define the schema for structured output
    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "id": {"type": "INTEGER"},
                    "category": {"type": "STRING", "enum": ["politics", "scam", "others"]}
                },
                "required": ["id", "category"]
            }
        }
    }

    model = genai.GenerativeModel(MODEL_NAME, generation_config=generation_config)

    try:
        response = model.generate_content(full_prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating content: {e}")
        return []

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # Ensure ID is integer
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)
    
    # Check if output file exists to resume or start over
    processed_ids = set()
    if os.path.exists(OUTPUT_FILE):
        try:
            existing_df = pd.read_csv(OUTPUT_FILE)
            if 'ID' in existing_df.columns:
                processed_ids = set(existing_df['ID'])
            print(f"Resuming... {len(processed_ids)} items already processed.")
        except Exception:
            print("Output file exists but could not be read. Starting fresh.")
    else:
        # Initialize output file with headers
        pd.DataFrame(columns=['ID', 'TITLE', 'LLM_CATEGORY']).to_csv(OUTPUT_FILE, index=False)

    # Filter out already processed items
    # We only need ID and TITLE for the API
    items_to_process = df[~df['ID'].isin(processed_ids)][['ID', 'TITLE']].to_dict('records')
    
    total_items = len(items_to_process)
    print(f"Total items to process: {total_items}")

    for i in range(0, total_items, BATCH_SIZE):
        batch = items_to_process[i:i+BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1}/{(total_items + BATCH_SIZE - 1)//BATCH_SIZE} ({len(batch)} items)...")
        
        results = categorize_batch(batch)
        
        if not results:
            print("Batch failed or returned empty. Skipping...")
            continue
            
        # Create a DataFrame for the results
        batch_results = []
        for res in results:
            # Find the title from the batch
            original_item = next((item for item in batch if item['ID'] == res['id']), None)
            if original_item:
                batch_results.append({
                    'ID': res['id'],
                    'TITLE': original_item['TITLE'],
                    'LLM_CATEGORY': res['category']
                })
        
        if batch_results:
            batch_df = pd.DataFrame(batch_results)
            # Append to CSV, skip header
            batch_df.to_csv(OUTPUT_FILE, mode='a', header=False, index=False)
            print(f"Saved {len(batch_df)} items to {OUTPUT_FILE}")
        
        # Rate limiting to be safe
        time.sleep(2)

    print("Done!")

if __name__ == "__main__":
    main()
