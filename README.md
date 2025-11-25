# Indonesian Hoax Analysis 2024

A comprehensive computational analysis of misinformation and disinformation patterns in Indonesia during the 2024 election period, based on fact-checking data from [turnbackhoax.id](http://turnbackhoax.id).

## 📖 Overview

This project systematically analyzes hoax patterns, sentiment trends, entity relationships, and thematic structures in Indonesian misinformation throughout 2024. Using advanced Natural Language Processing (NLP) and network analysis techniques, we examine **3,746 hoax articles** across three major categories: **Politics**, **Scam**, and **Others** (health, disasters, international conflicts).

### Research Context

The 2024 Indonesian General Election marked a critical moment for understanding misinformation dynamics:
- **185.3 million** active internet users (66.5% of population)
- **46%** of Indonesians get news from social media
- **203 cases** of election-related misinformation identified in January 2024 alone
- Primary platforms: WhatsApp (90.9%), Instagram (85.3%), Facebook (81.6%)

This analysis leverages data from **MAFINDO** (Masyarakat Antifitnah Indonesia), Indonesia's leading fact-checking organization, which has documented hoaxes since 2016 through their [turnbackhoax.id](http://turnbackhoax.id) platform.

## 🎯 Key Features

- **Multi-Category Analysis**: Automated LLM-based categorization of hoaxes into Politics, Scam, and Others
- **Sentiment Analysis**: Deep learning-based Indonesian sentiment classification using RoBERTa
- **Network Analysis**: Co-occurrence network analysis revealing entity relationships and narrative bridges
- **Topic Modeling**: LDA-based topic discovery across different hoax categories
- **Interactive Visualizations**: HTML-based network graphs, sentiment charts, and topic distributions

## 📊 Main Findings

### Politics (1,358 documents)
- **58-69%** negative sentiment across all political candidates
- **Anies Baswedan** serves as primary "bridge" entity connecting opposition narratives
- **5 distinct narrative communities**: Government influence, Electoral process, Fraud allegations, Opposition candidates, Media criticism
- High network density (0.323) suggests coordinated messaging patterns

### Scam (939 documents)
- **WhatsApp** (147) and **Facebook** (134) dominate as scam distribution platforms
- **Neutral sentiment** (75-95%) due to professional tone mimicking official communications
- **6 scam communities**: Banking fraud, Employment scams, Social media impersonation, E-wallet fraud
- Highest network interconnectedness (density: 0.378)

### Others (1,449 documents)
- **Natural disasters** most mentioned (Gempa: 97, Bencana: 90)
- **Israel-Palestine conflict** dominates international geopolitical hoaxes
- **COVID-19** and vaccine misinformation remains prevalent
- Lower network density (0.237) reflects diverse, less coordinated themes

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd <repository-name>
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

4. **Download NLTK data** (for text preprocessing)
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 📦 Project Structure

```
.
├── Scraping turnbackhoax.id - Complete.csv  # Raw scraped dataset (3,746 articles)
│
├── data_prep/                          # Data preparation and preprocessing
│   ├── [scraping_notebook.ipynb]     # Initial web scraping from turnbackhoax.id
│   ├── categorize_hoaxes.py           # LLM-based categorization
│   ├── add_llm_category.py            # Add categories to dataset
│   ├── clean_columns.py               # Data cleaning utilities
│   ├── extract_content.py             # Content extraction
│   ├── prepare_topic_modeling_data.py # Prepare data for LDA
│   └── categorized_hoaxes.csv         # Processed dataset with LLM categories
│
├── sentiment_analysis/                 # Sentiment analysis module
│   ├── sentiment_analysis.py          # Main sentiment analysis script
│   ├── visualize_sentiment.py         # Visualization generation
│   ├── analysis_report.md             # Detailed findings report
│   ├── sentiment_results.csv          # Full sentiment results
│   └── *.png                          # Sentiment distribution charts
│
├── text_network/                       # Network analysis module
│   ├── run_text_network_analysis.py   # Network construction & analysis
│   ├── run_multi_category_analysis.py # Multi-category comparison
│   ├── visualize_network.py           # Network visualization
│   ├── create_enhanced_multi_category.py # Enhanced visualizations
│   ├── README.md                      # Detailed network analysis report
│   └── network_analysis_results/      # Output files
│       ├── multi_category_network.html  # Interactive visualization
│       ├── top_entities.csv
│       ├── bridge_words.csv
│       └── communities.csv
│
├── topic_modeling/                     # Topic modeling module
│   ├── lda_analysis.py                # LDA model training
│   ├── run_lda_analysis.py            # Execute topic modeling
│   ├── visualize_topics.py            # Topic visualizations
│   ├── lda_visualization.html         # Interactive LDA explorer
│   └── [category]_category/           # Category-specific results
│       ├── topic_summary.csv
│       ├── topic_terms.csv
│       └── viz/                       # Topic visualizations
│
├── requirements.txt                    # Python dependencies
├── research_background.md             # Research context (Indonesian)
└── Scraping turnbackhoax.id - Complete.csv  # Raw dataset
```

## 🚀 Usage

### 0. Data Collection (Initial Scraping)

The raw dataset was collected through web scraping from [turnbackhoax.id](http://turnbackhoax.id):

**Output:**
- `Scraping turnbackhoax.id - Complete.csv` - Complete scraped dataset containing:
  - URL, Title, Category, Topic, Date, Author
  - Content (hoax text and fact-check explanation)
  - Image URL, ID
  - 3,746 fact-checked hoax articles from 2024

**Note**: If there's a Jupyter notebook for the scraping process in `data_prep/`, you can run it to update or re-scrape the data. The scraping notebook typically collects:
- Article metadata (title, date, author, category)
- Full content text (HOAX_TEXT and fact-check narratives)
- References and source URLs
- Images and supporting media

### 1. Data Preparation

**Categorize hoaxes using LLM:**
```bash
cd data_prep
python categorize_hoaxes.py
```

This script uses Google's Gemini API to automatically categorize each hoax into Politics, Scam, or Others based on content analysis.

**Add categories to the main dataset:**
```bash
python add_llm_category.py
```

### 2. Sentiment Analysis

**Run sentiment analysis:**
```bash
cd sentiment_analysis
python sentiment_analysis.py
```

**Generate visualizations:**
```bash
python visualize_sentiment.py
```

**Outputs:**
- `sentiment_results.csv` - Sentiment scores for all documents
- `candidate_sentiment_summary.csv` - Sentiment by political candidate
- `*_sentiment_distribution.png` - Bar charts showing sentiment distribution

**Model used:** `w11wo/indonesian-roberta-base-sentiment-classifier`

### 3. Network Analysis

**Run network analysis for all categories:**
```bash
cd text_network
python run_multi_category_analysis.py
```

**Generate interactive visualizations:**
```bash
python create_enhanced_multi_category.py
```

**Outputs:**
- `multi_category_network.html` - Interactive tabbed network visualization
- `top_entities.csv` - Ranked entities by centrality metrics
- `bridge_words.csv` - High betweenness centrality entities
- `communities.csv` - Community detection results
- `network_metadata.json` - Network statistics

**Key metrics calculated:**
- Degree Centrality
- Betweenness Centrality (identifies "bridge" entities)
- Eigenvector Centrality
- PageRank
- Community Detection (Greedy Modularity)

### 4. Topic Modeling

**Prepare data for topic modeling:**
```bash
cd topic_modeling
python prepare_topic_modeling_data.py
```

**Run LDA analysis:**
```bash
python run_lda_analysis.py
```

**Generate topic visualizations:**
```bash
python visualize_topics.py
```

**Outputs:**
- `lda_visualization.html` - Interactive pyLDAvis visualization
- `topic_summary.csv` - Topic distribution statistics
- `topic_terms.csv` - Top terms per topic
- `coherence_scores.csv` - Model coherence comparison
- `viz/` - Static visualizations (word clouds, topic distributions)

**Models trained:** LDA with 5, 7, and 10 topics (optimal selected by coherence score)

## 📈 Key Outputs

### 1. Sentiment Reports
- **HTML Report**: `sentiment_analysis/sentiment_report.html`
- **Analysis Report**: `sentiment_analysis/analysis_report.md`

### 2. Network Analysis
- **Interactive Visualization**: `text_network/network_analysis_results/multi_category_network.html`
- **Detailed Report**: `text_network/README.md`

### 3. Topic Models
- **Interactive LDA**: `topic_modeling/lda_visualization.html`
- **Complete Analysis**: `topic_modeling/COMPLETE_ANALYSIS_SUMMARY.md`

## 🔍 Methodology

### Data Source
- **Platform**: [turnbackhoax.id](http://turnbackhoax.id) (MAFINDO)
- **Period**: January - December 2024
- **Total Documents**: 3,746 hoax articles
- **Categories**: Politics (1,358), Scam (939), Others (1,449)

### Analysis Pipeline

1. **Data Collection**: Web scraping hoax articles and fact-check reports from turnbackhoax.id
   - Source: MAFINDO's fact-checking platform
   - Fields: URL, Title, Category, Content, Date, Author, Images
   - Output: `Scraping turnbackhoax.id - Complete.csv`
   
2. **Preprocessing**: Text cleaning, tokenization, stopword removal (Sastrawi)
   - Indonesian-specific text normalization
   - Remove punctuation, numbers, special characters
   - Sastrawi stemmer for Indonesian language
   
3. **Categorization**: LLM-based classification using Google Gemini
   - Automated categorization into Politics, Scam, Others
   - Prompt engineering for accurate classification
   - Output: `categorized_hoaxes.csv`
   
4. **Sentiment Analysis**: Indonesian RoBERTa model for sentiment classification
   - Model: `w11wo/indonesian-roberta-base-sentiment-classifier`
   - Labels: Positive, Negative, Neutral
   - Entity-level sentiment aggregation
   
5. **Entity Extraction**: Keyword-based entity identification and matching
   - Predefined dictionaries for Politics, Scam, Others categories
   - Pattern matching in HOAX_TEXT content
   - Co-occurrence tracking
   
6. **Network Construction**: Co-occurrence networks with minimum threshold
   - Nodes: Entities (politicians, platforms, topics)
   - Edges: Co-occurrence within same document
   - Minimum threshold: 2 co-occurrences
   
7. **Community Detection**: Greedy modularity optimization
   - Identify narrative clusters and themes
   - Calculate centrality metrics (degree, betweenness, eigenvector, PageRank)
   - Detect bridge entities connecting different narratives
   
8. **Topic Modeling**: LDA with coherence score optimization
   - Models trained with 5, 7, and 10 topics
   - Optimal model selected by coherence score
   - pyLDAvis for interactive visualization

### Technical Stack

- **NLP**: Transformers (Hugging Face), Sastrawi, NLTK
- **LLM**: Google Gemini API
- **Topic Modeling**: Gensim, pyLDAvis
- **Network Analysis**: NetworkX
- **Visualization**: Matplotlib, Seaborn, Plotly, Pyvis
- **Data Processing**: Pandas, NumPy

## 📚 Dependencies

```
pandas>=2.0.0
google-generativeai
python-dotenv
gensim>=4.3.0
pyLDAvis>=3.4.0
Sastrawi>=1.2.0
nltk>=3.8.0
matplotlib>=3.7.0
seaborn>=0.12.0
wordcloud>=1.9.0
scipy>=1.11.0
numpy>=1.24.0
transformers>=4.30.0
torch>=2.0.0
networkx>=3.0
pyvis>=0.3.0
```

## 🎓 Research Applications

This analysis can support:
- **Misinformation Research**: Understanding Indonesian hoax patterns and narratives
- **Political Communication**: Analyzing campaign-related disinformation
- **Digital Literacy**: Identifying common scam tactics and platforms
- **Policy Making**: Evidence-based approaches to combat misinformation
- **Journalism**: Fact-checking insights and trend analysis

## 📝 Citation

If you use this work in your research, please cite:

```bibtex
@misc{indonesian_hoax_analysis_2024,
  title={Indonesian Hoax Analysis 2024: A Computational Study of Misinformation Patterns},
  author={[Your Name]},
  year={2024},
  howpublished={GitHub Repository},
  url={[repository-url]}
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- **MAFINDO** (Masyarakat Antifitnah Indonesia) for maintaining [turnbackhoax.id](http://turnbackhoax.id)
- **International Fact-Checking Network** for supporting Indonesian fact-checking efforts
- **We Are Social** and **Reuters Institute** for providing digital landscape data

## 📧 Contact

[Your contact information]

---

**Note**: This project analyzes publicly available fact-checking data for research purposes. All original hoax content has been debunked by professional fact-checkers at MAFINDO.
