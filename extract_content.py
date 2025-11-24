import pandas as pd
import re
import sys

def parse_content(text):
    if not isinstance(text, str):
        return {}
    
    # Regex to find tags like [TAG]
    # Captures the tag name (without brackets)
    # We use a lookahead or split approach.
    # re.split with capturing group returns [text_before, tag, text_after, tag, text_after...]
    
    # Pattern to find tags:
    # 1. [TAG] -> \[([A-Z\s]+)\]
    # 2. TAG : -> ([A-Z]+)\s*:
    # We combine them. We need to be careful not to match normal words.
    # The "TAG :" format usually has specific keywords like SUMBER, NARASI, PENJELASAN.
    # Let's try to match the specific ones we know or just Capitalized words followed by colon.
    # But "FAKTA :" might appear in text.
    # Let's stick to the user's list plus common ones if possible, or just use a generic pattern and filter later.
    # Given the plan mentions "Narasi:...", let's try to capture that.
    
    # Regex:
    # \[([A-Z\s]+)\]  <-- matches [TAG]
    # |
    # \b([A-Z]+)\s*:  <-- matches TAG : (word boundary start)
    
    pattern = r'(?:\[([A-Z\s]+)\]|\b([A-Z]+)\s*:)'
    
    # re.split will return None for the non-matching group in the pair.
    # e.g. if [TAG] matches, group 1 is TAG, group 2 is None.
    parts = re.split(pattern, text)
    
    # parts structure will be:
    # [text, tag1_group1, tag1_group2, text, tag2_group1, tag2_group2, text...]
    
    result = {}
    
    # Iterate with step 3 because each split adds 2 capturing groups + 1 text chunk
    # parts[0] = text before first tag
    # parts[1] = group 1 (bracketed)
    # parts[2] = group 2 (colon)
    # parts[3] = text after first tag
    
    for i in range(1, len(parts), 3):
        tag_bracket = parts[i]
        tag_colon = parts[i+1]
        content = parts[i+2].strip() if i+2 < len(parts) else ""
        
        tag = tag_bracket if tag_bracket else tag_colon
        if tag:
            tag = tag.strip()
            result[tag] = content
            
    return result

def main():
    input_file = "Scraping turnbackhoax.id - Complete.csv"
    output_file = "Scraping turnbackhoax.id - Structured.csv"
    
    print(f"Reading {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
        
    if 'CONTENT' not in df.columns:
        print("Error: 'CONTENT' column not found.")
        sys.exit(1)
        
    print("Extracting content structure...")
    # Apply parsing
    extracted_data = df['CONTENT'].apply(parse_content)
    
    # Convert list of dicts to DataFrame
    extracted_df = pd.DataFrame(extracted_data.tolist())
    
    # Column merging logic
    print("Refining columns...")
    
    # Combine NARASI and NARASII (if exists)
    if 'NARASII' in extracted_df.columns:
        if 'NARASI' not in extracted_df.columns:
            extracted_df['NARASI'] = extracted_df['NARASII']
        else:
            extracted_df['NARASI'] = extracted_df['NARASI'].combine_first(extracted_df['NARASII'])
            
    # Combine FAKTA and FAKTANYA (if exists) -> into FAKTA
    # Note: FAKTA might not exist yet
    if 'FAKTA' not in extracted_df.columns:
        extracted_df['FAKTA'] = None
        
    if 'FAKTANYA' in extracted_df.columns:
        extracted_df['FAKTA'] = extracted_df['FAKTA'].combine_first(extracted_df['FAKTANYA'])
        
    # Define columns to keep
    target_columns = ['KATEGORI', 'SUMBER', 'NARASI', 'PENJELASAN', 'REFERENSI', 'FAKTA', 'SALAH']
    
    # Ensure all target columns exist (fill with NaN if missing)
    for col in target_columns:
        if col not in extracted_df.columns:
            extracted_df[col] = None
            
    # Filter extracted_df to only these columns
    extracted_df = extracted_df[target_columns]
    
    # Merge with original DataFrame
    # We want to keep original columns and add new ones
    result_df = pd.concat([df, extracted_df], axis=1)
    
    print(f"Extracted columns kept: {extracted_df.columns.tolist()}")
    
    print(f"Saving to {output_file}...")
    result_df.to_csv(output_file, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
