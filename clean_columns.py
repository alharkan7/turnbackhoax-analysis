import pandas as pd
import re
import sys

def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # 1. Strip whitespace
    text = text.strip()
    
    # 2. Remove leading colon and whitespace (e.g., ": ")
    # Repeat until no more leading colons (just in case)
    text = re.sub(r'^[:\s]+', '', text)
    
    # 3. Remove trailing equals signs and whitespace (e.g., " =======")
    text = re.sub(r'[\s=]+$', '', text)
    
    # 4. Remove enclosing quotes
    # Handle straight quotes " and smart quotes “ ”
    # Check if starts and ends with quotes
    
    # Simple strip of quotes might be dangerous if it's not matching, 
    # but user said "if the text are enclosed within".
    # Let's try to match pairs or just strip leading/trailing quote characters.
    # Often it's just one quote at start if the CSV parsing was weird, or real quotes.
    # Let's strip leading/trailing quote chars.
    text = text.strip('"“”')
    
    # 5. Final strip
    text = text.strip()
    
    return text

def main():
    input_file = "Scraping turnbackhoax.id - Structured.csv"
    output_file = "Scraping turnbackhoax.id - Cleaned.csv"
    
    columns_to_clean = [
        'KATEGORI', 'SUMBER', 'NARASI', 'PENJELASAN', 
        'REFERENSI', 'FAKTA', 'SALAH'
    ]
    
    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
        
    print("Cleaning columns...")
    for col in columns_to_clean:
        if col in df.columns:
            print(f"Cleaning {col}...")
            df[col] = df[col].apply(clean_text)
            
    print(f"Saving to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
