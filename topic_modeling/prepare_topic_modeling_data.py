#!/usr/bin/env python3
"""
Prepare data for Topic Modeling by extracting HOAX_TEXT from CONTENT.
This script extracts the NARASI (hoax narrative) from the CONTENT field,
filters for politics category, and creates a clean dataset for LDA analysis.
"""

import pandas as pd
import re
import sys

def extract_narasi(content_text, title_fallback):
    """
    Extract NARASI (hoax narrative) from CONTENT field.
    
    Args:
        content_text: The CONTENT column text
        title_fallback: The TITLE to use if NARASI not found
        
    Returns:
        Extracted hoax text (NARASI or TITLE fallback)
    """
    if not isinstance(content_text, str):
        return title_fallback
    
    # Try to find [NARASI] tag
    # Pattern matches: [NARASI] ... [next tag or end]
    narasi_pattern = r'\[NARASI\]\s*:?\s*(.*?)(?:\[|$)'
    match = re.search(narasi_pattern, content_text, re.IGNORECASE | re.DOTALL)
    
    if match:
        narasi_text = match.group(1).strip()
        # Clean up common separators
        narasi_text = re.sub(r'={3,}.*?={3,}', '', narasi_text)  # Remove ======
        narasi_text = narasi_text.strip()
        if narasi_text and len(narasi_text) > 10:
            return narasi_text
    
    # Try alternative pattern: NARASI: or Narasi:
    narasi_pattern2 = r'(?:NARASI|Narasi)\s*:\s*(.*?)(?:\[|={3}|$)'
    match = re.search(narasi_pattern2, content_text, re.DOTALL)
    
    if match:
        narasi_text = match.group(1).strip()
        narasi_text = re.sub(r'={3,}.*?={3,}', '', narasi_text)
        narasi_text = narasi_text.strip()
        if narasi_text and len(narasi_text) > 10:
            return narasi_text
    
    # Fallback to TITLE as mentioned in the plan
    return title_fallback

def main():
    print("=" * 60)
    print("PREPARING DATA FOR TOPIC MODELING")
    print("=" * 60)
    
    # File paths
    original_csv = "Scraping turnbackhoax.id - Complete.csv"
    categorized_csv = "data_prep/categorized_hoaxes.csv"
    output_csv = "topic_modeling/politics_hoax_text.csv"
    
    # Load original data with all columns
    print(f"\n[1/5] Loading original dataset: {original_csv}")
    try:
        df_original = pd.read_csv(original_csv)
        print(f"   ✓ Loaded {len(df_original)} rows")
        print(f"   Columns: {df_original.columns.tolist()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        sys.exit(1)
    
    # Load categorized data (ID + LLM_CATEGORY)
    print(f"\n[2/5] Loading categorized data: {categorized_csv}")
    try:
        df_categorized = pd.read_csv(categorized_csv)
        print(f"   ✓ Loaded {len(df_categorized)} categorized rows")
        print(f"   Categories: {df_categorized['LLM_CATEGORY'].value_counts().to_dict()}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        sys.exit(1)
    
    # Merge to get LLM_CATEGORY for original data
    print(f"\n[3/5] Merging datasets on ID...")
    df_merged = df_original.merge(df_categorized[['ID', 'LLM_CATEGORY']], on='ID', how='inner')
    print(f"   ✓ Merged dataset: {len(df_merged)} rows")
    
    # Filter for politics only
    print(f"\n[4/5] Filtering for politics category...")
    df_politics = df_merged[df_merged['LLM_CATEGORY'] == 'politics'].copy()
    print(f"   ✓ Politics subset: {len(df_politics)} rows")
    
    # Extract HOAX_TEXT from CONTENT
    print(f"\n[5/5] Extracting HOAX_TEXT from CONTENT...")
    df_politics['HOAX_TEXT'] = df_politics.apply(
        lambda row: extract_narasi(row['CONTENT'], row['TITLE']),
        axis=1
    )
    
    # Check extraction success
    # Count how many used NARASI vs TITLE fallback
    narasi_count = df_politics['HOAX_TEXT'].apply(
        lambda x: '[NARASI]' in str(df_politics[df_politics['HOAX_TEXT'] == x]['CONTENT'].iloc[0] if len(df_politics[df_politics['HOAX_TEXT'] == x]) > 0 else '')
    ).sum()
    
    print(f"   ✓ Extracted HOAX_TEXT for all rows")
    print(f"   - Average length: {df_politics['HOAX_TEXT'].str.len().mean():.0f} characters")
    print(f"   - Min length: {df_politics['HOAX_TEXT'].str.len().min()}")
    print(f"   - Max length: {df_politics['HOAX_TEXT'].str.len().max()}")
    
    # Select relevant columns for topic modeling
    df_output = df_politics[['ID', 'TITLE', 'DATE', 'HOAX_TEXT', 'LLM_CATEGORY']].copy()
    
    # Save to CSV
    print(f"\n[OUTPUT] Saving to: {output_csv}")
    df_output.to_csv(output_csv, index=False)
    print(f"   ✓ Saved {len(df_output)} rows for topic modeling")
    
    # Show sample
    print(f"\n[SAMPLE] First 3 HOAX_TEXT extracts:")
    print("-" * 60)
    for idx, row in df_output.head(3).iterrows():
        print(f"\nID {row['ID']}: {row['TITLE'][:60]}...")
        print(f"HOAX_TEXT: {row['HOAX_TEXT'][:200]}...")
    
    print("\n" + "=" * 60)
    print("✓ DATA PREPARATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
