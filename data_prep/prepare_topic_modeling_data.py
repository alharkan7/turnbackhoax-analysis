#!/usr/bin/env python3
"""
Prepare data for Topic Modeling by extracting HOAX_TEXT from CONTENT.
This script extracts the NARASI (hoax narrative) from the CONTENT field,
filters by category, and creates a clean dataset for LDA analysis.

Usage:
    python3 prepare_topic_modeling_data.py <category> <output_dir>
    
    category: politics, scam, or others
    output_dir: directory to save output (e.g., topic_modeling/scam_category)
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
    if len(sys.argv) != 3:
        print("Usage: python3 prepare_topic_modeling_data.py <category> <output_dir>")
        print("  category: politics, scam, or others")
        print("  output_dir: directory to save output")
        sys.exit(1)
    
    category = sys.argv[1].lower()
    output_dir = sys.argv[2]
    
    if category not in ['politics', 'scam', 'others']:
        print(f"Error: category must be 'politics', 'scam', or 'others', got '{category}'")
        sys.exit(1)
    
    print("=" * 60)
    print(f"PREPARING DATA FOR TOPIC MODELING - {category.upper()}")
    print("=" * 60)
    
    # File paths
    original_csv = "Scraping turnbackhoax.id - Complete.csv"
    categorized_csv = "data_prep/categorized_hoaxes.csv"
    output_csv = f"{output_dir}/{category}_hoax_text.csv"
    
    # Load original data with all columns
    print(f"\n[1/5] Loading original dataset: {original_csv}")
    try:
        df_original = pd.read_csv(original_csv)
        print(f"   ✓ Loaded {len(df_original)} rows")
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
    
    # Filter for specified category
    print(f"\n[4/5] Filtering for '{category}' category...")
    df_category = df_merged[df_merged['LLM_CATEGORY'] == category].copy()
    print(f"   ✓ {category.title()} subset: {len(df_category)} rows")
    
    if len(df_category) == 0:
        print(f"   ✗ No data found for category '{category}'")
        sys.exit(1)
    
    # Extract HOAX_TEXT from CONTENT
    print(f"\n[5/5] Extracting HOAX_TEXT from CONTENT...")
    df_category['HOAX_TEXT'] = df_category.apply(
        lambda row: extract_narasi(row['CONTENT'], row['TITLE']),
        axis=1
    )
    
    print(f"   ✓ Extracted HOAX_TEXT for all rows")
    print(f"   - Average length: {df_category['HOAX_TEXT'].str.len().mean():.0f} characters")
    print(f"   - Min length: {df_category['HOAX_TEXT'].str.len().min()}")
    print(f"   - Max length: {df_category['HOAX_TEXT'].str.len().max()}")
    
    # Select relevant columns for topic modeling
    df_output = df_category[['ID', 'TITLE', 'DATE', 'HOAX_TEXT', 'LLM_CATEGORY']].copy()
    
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
