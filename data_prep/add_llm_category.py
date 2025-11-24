import pandas as pd

# Read the categorized hoaxes file to create ID to LLM_CATEGORY mapping
categorized_df = pd.read_csv('categorized_hoaxes.csv')
id_to_category = dict(zip(categorized_df['ID'], categorized_df['LLM_CATEGORY']))

# Read the main scraping file
scraping_df = pd.read_csv('Scraping turnbackhoax.id - Complete.csv')

# Add the LLM Category column by mapping IDs
scraping_df['LLM Category'] = scraping_df['ID'].map(id_to_category)

# Save the updated file
scraping_df.to_csv('Scraping turnbackhoax.id - Complete.csv', index=False)

print(f"Successfully added LLM Category column to {len(scraping_df)} rows")
print("File saved as 'Scraping turnbackhoax.id - Complete.csv'")


