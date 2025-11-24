import pandas as pd
import re
import sys

# --- Extraction Logic (from extract_content.py) ---
def parse_content(text):
    if not isinstance(text, str):
        return {}
    
    # Regex to find tags like [TAG] or TAG:
    pattern = r'(?:\[([A-Z\s]+)\]|\b([A-Z]+)\s*:)'
    parts = re.split(pattern, text)
    
    result = {}
    # Iterate with step 3 because each split adds 2 capturing groups + 1 text chunk
    for i in range(1, len(parts), 3):
        tag_bracket = parts[i]
        tag_colon = parts[i+1]
        content = parts[i+2].strip() if i+2 < len(parts) else ""
        
        tag = tag_bracket if tag_bracket else tag_colon
        if tag:
            tag = tag.strip()
            result[tag] = content
            
    return result

# --- Cleaning Logic (from clean_columns.py) ---
def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # 1. Strip whitespace
    text = text.strip()
    # 2. Remove leading colon and whitespace
    text = re.sub(r'^[:\s]+', '', text)
    # 3. Remove trailing equals signs and whitespace
    text = re.sub(r'[\s=]+$', '', text)
    # 4. Remove enclosing quotes
    text = text.strip('"“”')
    # 5. Final strip
    text = text.strip()
    
    return text

# --- Categorization Logic ---
def categorize_text(text):
    if not isinstance(text, str):
        return 'Other'
    
    text_lower = text.lower()
    
    # Keywords for Scams (Bucket B) - Check FIRST to remove noise
    scam_keywords = [
        'undian', 'hadiah', 'bank', 'bri', 'bni', 'mandiri', 'bca', 'saldo', 
        'giveaway', 'dana kaget', 'kuota', 'pulsa', 'internet gratis', 
        'lowongan', 'loker', 'rekrutmen', 'bumn', 'pln', 'pertamina', 
        'bpjs', 'bansos', 'blt', 'prakerja', 'promo', 'tebus murah'
    ]
    
    for keyword in scam_keywords:
        if keyword in text_lower:
            return 'Scam'
            
    # Keywords for Politics (Bucket A)
    politics_keywords = [
        'prabowo', 'gibran', 'anies', 'ganjar', 'jokowi', 'kpu', 'bawaslu', 
        'pemilu', 'curang', 'mk', 'partai', 'pilpres', 'capres', 'cawapres', 
        'koalisi', 'debat', 'kampanye', 'tps', 'surat suara', 'kotak suara', 
        'penghitungan', 'sirekap', 'hak angket', 'mahkamah konstitusi', 
        'politik', 'presiden', 'wakil presiden'
    ]
    
    for keyword in politics_keywords:
        if keyword in text_lower:
            return 'Politics'
            
    return 'Other'

def main():
    input_file = "Scraping turnbackhoax.id - Complete.csv"
    output_politics = "politics_hoaxes.csv"
    
    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
        
    print("Processing content (Extraction & Cleaning)...")
    
    # 1. Extract Structure
    if 'CONTENT' in df.columns:
        extracted_data = df['CONTENT'].apply(parse_content)
        extracted_df = pd.DataFrame(extracted_data.tolist())
        
        # Merge extracted columns back to df temporarily to handle logic
        # We mainly care about NARASI
        if 'NARASI' in extracted_df.columns:
            df['NARASI'] = extracted_df['NARASI']
        else:
            df['NARASI'] = None
            
        if 'NARASII' in extracted_df.columns:
            df['NARASI'] = df['NARASI'].combine_first(extracted_df['NARASII'])
            
    else:
        print("Warning: CONTENT column not found.")
        df['NARASI'] = None

    # 2. Create HOAX_TEXT (Clean NARASI or Fallback to TITLE)
    print("Creating HOAX_TEXT...")
    
    # Helper to get the raw text source
    def get_raw_hoax_text(row):
        if pd.notna(row['NARASI']) and str(row['NARASI']).strip():
            return str(row['NARASI'])
        return str(row['TITLE'])

    df['HOAX_TEXT_RAW'] = df.apply(get_raw_hoax_text, axis=1)
    
    # 3. Clean it
    df['HOAX_TEXT'] = df['HOAX_TEXT_RAW'].apply(clean_text)
    
    # 4. Categorize
    print("Categorizing data...")
    df['CATEGORY_TAG'] = df['HOAX_TEXT'].apply(categorize_text)
    
    # Print statistics
    counts = df['CATEGORY_TAG'].value_counts()
    print("\nCategory Distribution:")
    print(counts)
    
    # Filter and save Politics bucket
    politics_df = df[df['CATEGORY_TAG'] == 'Politics']
    print(f"Saving {len(politics_df)} political hoaxes to {output_politics}...")
    politics_df.to_csv(output_politics, index=False)

    # Filter and save Scam bucket
    scam_df = df[df['CATEGORY_TAG'] == 'Scam']
    output_scam = "scam_hoaxes.csv"
    print(f"Saving {len(scam_df)} scam hoaxes to {output_scam}...")
    scam_df.to_csv(output_scam, index=False)

    # Filter and save Other bucket
    other_df = df[df['CATEGORY_TAG'] == 'Other']
    output_other = "other_hoaxes.csv"
    print(f"Saving {len(other_df)} other hoaxes to {output_other}...")
    other_df.to_csv(output_other, index=False)
    
    print("Done.")

if __name__ == "__main__":
    main()
