# Hoax Analysis Research Paper

## Overview
This project provides a comprehensive analysis of Indonesian hoax data from fact-checking websites. The analysis covers temporal trends, thematic patterns, entity analysis, and category dynamics to understand the characteristics and patterns of misinformation in Indonesia.

## Files Structure
- `scraping_data.csv` - Raw hoax data from fact-checking websites
- `hoax_analysis_notebook.ipynb` - Main analysis notebook
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Data Structure
The dataset contains the following columns:
- **URL**: Link to the fact-checking article
- **TITLE**: Title of the hoax/fact-check
- **CATEGORY**: Classification (SALAH, MENYESATKAN, etc.)
- **TOPIC**: Topic/category of the hoax
- **DATE**: Publication date
- **AUTHOR**: Fact-checker name
- **CONTENT**: Detailed fact-checking content
- **IMAGE URL**: Associated image link
- **ID**: Unique identifier

## Analysis Components

### 1. Temporal Analysis
- Monthly and daily hoax volume trends
- Annotation of major events (Pemilu 2024, Ramadan)
- Time series visualization

### 2. Thematic Analysis
- Top 10 most frequent topics
- WordCloud visualization of topics
- Topic co-occurrence analysis

### 3. Entity Analysis
- Named Entity Recognition for Indonesian political figures
- Top 15 most mentioned entities
- Entity frequency analysis

### 4. Category Dynamics
- Distribution of hoax categories
- Category trends over time
- Category x Topic cross-tabulation
- Category x Entity analysis

### 5. Author Analysis
- Most active fact-checkers
- Author contribution patterns

## Installation and Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have Jupyter Notebook installed:
```bash
pip install jupyter
```

3. Start Jupyter Notebook:
```bash
jupyter notebook
```

4. Open `hoax_analysis_notebook.ipynb` and run all cells

## Output Files

The analysis generates several output files:

### Data Files
- `cleaned_hoax_data.csv` - Processed dataset
- `extracted_entities.csv` - Extracted entities with frequencies
- `analysis_summary.csv` - Summary statistics

### Visualization Files
- `monthly_hoax_trends.png` - Monthly trend line chart
- `daily_hoax_trends.png` - Daily trend visualization
- `top_topics.png` - Top 10 topics bar chart
- `topic_wordcloud.png` - Topic word cloud
- `top_entities.png` - Top 15 entities chart
- `category_distribution.png` - Category pie chart
- `category_trends.png` - Category trends over time
- `category_topic_heatmap.png` - Category x Topic heatmap
- `entity_category_heatmap.png` - Entity x Category heatmap
- `topic_entity_heatmap.png` - Topic x Entity heatmap
- `top_authors.png` - Top fact-checkers chart

## Key Findings

The analysis reveals:
1. **Temporal Patterns**: Seasonal variations and event-driven spikes
2. **Thematic Focus**: Most common hoax topics and categories
3. **Entity Targeting**: Which political figures and organizations are most frequently targeted
4. **Category Evolution**: How different types of misinformation change over time
5. **Fact-checking Patterns**: Author contributions and verification approaches

## Research Applications

This analysis supports:
- Understanding misinformation patterns in Indonesian media
- Identifying high-risk topics and entities
- Temporal analysis of hoax propagation
- Policy recommendations for fact-checking organizations
- Academic research on digital misinformation

## Technical Notes

- The analysis uses regex-based entity extraction for Indonesian political figures
- Temporal analysis includes major political events annotation
- All visualizations are optimized for research paper inclusion
- Data cleaning handles missing values and format standardization

## Citation

If using this analysis in academic work, please cite:
```
Hoax Analysis Research Paper - Indonesian Fact-Checking Data Analysis
[Your Name/Institution]
[Year]
```

## Contact

For questions or collaboration opportunities, please contact [your contact information]. 