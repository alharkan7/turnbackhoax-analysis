#!/usr/bin/env python3
"""
LDA Topic Modeling Analysis for Political Hoaxes.

This script performs Latent Dirichlet Allocation (LDA) topic modeling on the
extracted political hoax narratives from turnbackhoax.id.

Features:
- Indonesian text preprocessing with Sastrawi stemmer
- Custom Indonesian stopwords
- Bigram detection for multi-word phrases
- Multiple topic configurations (5, 7, 10 topics)
- Coherence score evaluation
- Interactive pyLDAvis visualization
"""

import pandas as pd
import numpy as np
import re
import pickle
from pathlib import Path

# Gensim for LDA
from gensim import corpora
from gensim.models import LdaModel, CoherenceModel, Phrases
from gensim.models.phrases import Phraser

# Sastrawi for Indonesian stemming
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# PyLDAvis for visualization
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

class IndonesianLDAAnalyzer:
    """LDA Topic Modeling for Indonesian political hoax texts."""
    
    def __init__(self, data_path, output_dir="topic_modeling"):
        """
        Initialize the LDA analyzer.
        
        Args:
            data_path: Path to CSV with HOAX_TEXT column
            output_dir: Directory to save outputs
        """
        self.data_path = data_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Indonesian NLP tools
        self.stemmer = StemmerFactory().create_stemmer()
        self.stopword_factory = StopWordRemoverFactory()
        
        # Custom Indonesian stopwords (from analysis plan)
        self.custom_stopwords = {
            'dan', 'yang', 'di', 'ke', 'dari', 'video', 'foto', 'ini', 'itu',
            'hoax', 'cek', 'fakta', 'berita', 'informasi', 'konten', 'tersebut',
            'dengan', 'pada', 'untuk', 'adalah', 'oleh', 'dalam', 'akan',
            'telah', 'sudah', 'ada', 'juga', 'tidak', 'atau', 'bahwa', 'nya',
            'kami', 'kita', 'mereka', 'anda', 'dia', 'saya', 'ia', 'aku',
            'bisa', 'dapat', 'masih', 'hanya', 'lebih', 'sangat', 'paling',
            'saat', 'waktu', 'tahun', 'hari', 'bulan', 'tanggal', 'jam',
            'seperti', 'tentang', 'sebagai', 'antara', 'melalui', 'terhadap',
            'karena', 'sehingga', 'maka', 'jika', 'kalau', 'bila',
            'viral', 'beredar', 'menyebar', 'klaim', 'narasi', 'unggahan',
            'media', 'sosial', 'facebook', 'twitter', 'instagram', 'tiktok',
            'whatsapp', 'youtube', 'link', 'sumber', 'post', 'share'
        }
        
        # Combine with Sastrawi stopwords
        sastrawi_stopwords = set(self.stopword_factory.get_stop_words())
        self.all_stopwords = self.custom_stopwords.union(sastrawi_stopwords)
        
        # Storage
        self.df = None
        self.processed_docs = None
        self.dictionary = None
        self.corpus = None
        self.models = {}
        self.coherence_scores = {}
        
    def load_data(self):
        """Load the dataset."""
        print(f"\n[1/7] Loading data from {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        print(f"   ✓ Loaded {len(self.df)} documents")
        print(f"   Columns: {self.df.columns.tolist()}")
        
        # Check for missing HOAX_TEXT
        missing = self.df['HOAX_TEXT'].isna().sum()
        if missing > 0:
            print(f"   ⚠ Warning: {missing} documents have missing HOAX_TEXT")
            self.df = self.df.dropna(subset=['HOAX_TEXT'])
            print(f"   Remaining: {len(self.df)} documents")
    
    def preprocess_text(self, text):
        """
        Preprocess a single text document.
        
        Args:
            text: Raw text string
            
        Returns:
            List of cleaned, stemmed tokens
        """
        if not isinstance(text, str):
            return []
        
        # Lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and numbers, keep only letters and spaces
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = text.split()
        
        # Remove stopwords
        tokens = [t for t in tokens if t not in self.all_stopwords and len(t) > 2]
        
        # Stem with Sastrawi
        tokens = [self.stemmer.stem(t) for t in tokens]
        
        # Remove duplicates while preserving order
        seen = set()
        tokens = [t for t in tokens if not (t in seen or seen.add(t))]
        
        return tokens
    
    def preprocess_corpus(self):
        """Preprocess all documents in the corpus."""
        print(f"\n[2/7] Preprocessing corpus...")
        print("   - Tokenizing")
        print("   - Removing stopwords")
        print("   - Stemming with Sastrawi")
        
        self.processed_docs = []
        for idx, text in enumerate(self.df['HOAX_TEXT']):
            tokens = self.preprocess_text(text)
            self.processed_docs.append(tokens)
            
            if (idx + 1) % 200 == 0:
                print(f"   Processed {idx + 1}/{len(self.df)} documents...", end='\r')
        
        print(f"\n   ✓ Preprocessed {len(self.processed_docs)} documents")
        
        # Calculate average tokens per document
        avg_tokens = np.mean([len(doc) for doc in self.processed_docs])
        print(f"   Average tokens per document: {avg_tokens:.1f}")
    
    def build_bigrams(self):
        """Build bigram models for multi-word phrases."""
        print(f"\n[3/7] Building bigram models...")
        print("   Detecting phrases like: 'TKA China', 'Surat Suara', etc.")
        
        # Build bigram model
        bigram = Phrases(self.processed_docs, min_count=5, threshold=10)
        bigram_mod = Phraser(bigram)
        
        # Apply bigrams to documents
        self.processed_docs = [bigram_mod[doc] for doc in self.processed_docs]
        
        # Show some detected bigrams
        sample_bigrams = [token for doc in self.processed_docs[:100] 
                         for token in doc if '_' in token]
        unique_bigrams = list(set(sample_bigrams))[:10]
        
        print(f"   ✓ Built bigram models")
        if unique_bigrams:
            print(f"   Sample bigrams detected: {', '.join(unique_bigrams)}")
    
    def create_dictionary_corpus(self):
        """Create dictionary and corpus for LDA."""
        print(f"\n[4/7] Creating dictionary and corpus...")
        
        # Create Dictionary
        self.dictionary = corpora.Dictionary(self.processed_docs)
        
        print(f"   Dictionary before filtering: {len(self.dictionary)} unique tokens")
        
        # Filter extremes
        # Remove words that appear in < 2 documents or > 50% of documents
        self.dictionary.filter_extremes(no_below=2, no_above=0.5)
        
        print(f"   Dictionary after filtering: {len(self.dictionary)} unique tokens")
        
        # Create Corpus (Bag of Words)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in self.processed_docs]
        
        print(f"   ✓ Created corpus with {len(self.corpus)} documents")
        
        # Save dictionary
        dict_path = self.output_dir / "dictionary.pkl"
        with open(dict_path, 'wb') as f:
            pickle.dump(self.dictionary, f)
        print(f"   Saved dictionary to {dict_path}")
    
    def train_lda_models(self, topic_numbers=[5, 7, 10]):
        """
        Train LDA models with different numbers of topics.
        
        Args:
            topic_numbers: List of topic counts to try
        """
        print(f"\n[5/7] Training LDA models...")
        print(f"   Testing topic numbers: {topic_numbers}")
        
        for num_topics in topic_numbers:
            print(f"\n   Training model with {num_topics} topics...")
            
            # Train LDA model
            lda_model = LdaModel(
                corpus=self.corpus,
                id2word=self.dictionary,
                num_topics=num_topics,
                random_state=42,
                update_every=1,
                chunksize=100,
                passes=10,
                alpha='auto',
                per_word_topics=True,
                iterations=100
            )
            
            # Calculate coherence score
            coherence_model = CoherenceModel(
                model=lda_model,
                texts=self.processed_docs,
                dictionary=self.dictionary,
                coherence='c_v'
            )
            coherence_score = coherence_model.get_coherence()
            
            # Store model and score
            self.models[num_topics] = lda_model
            self.coherence_scores[num_topics] = coherence_score
            
            print(f"   ✓ Coherence Score: {coherence_score:.4f}")
            
            # Save model
            model_path = self.output_dir / f"lda_model_{num_topics}topics.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(lda_model, f)
            print(f"   Saved model to {model_path}")
        
        # Save coherence scores
        coherence_df = pd.DataFrame({
            'num_topics': list(self.coherence_scores.keys()),
            'coherence_score': list(self.coherence_scores.values())
        })
        coherence_path = self.output_dir / "coherence_scores.csv"
        coherence_df.to_csv(coherence_path, index=False)
        print(f"\n   ✓ Saved coherence scores to {coherence_path}")
        
        # Identify best model
        best_num_topics = max(self.coherence_scores, key=self.coherence_scores.get)
        print(f"\n   🏆 Best model: {best_num_topics} topics (coherence: {self.coherence_scores[best_num_topics]:.4f})")
        
        return best_num_topics
    
    def generate_visualizations(self, best_num_topics):
        """Generate visualizations for the best model."""
        print(f"\n[6/7] Generating visualizations for {best_num_topics}-topic model...")
        
        best_model = self.models[best_num_topics]
        
        # PyLDAvis interactive visualization
        print("   Creating interactive pyLDAvis visualization...")
        vis_data = gensimvis.prepare(best_model, self.corpus, self.dictionary, mds='mmds')
        
        html_path = self.output_dir / "lda_visualization.html"
        pyLDAvis.save_html(vis_data, str(html_path))
        print(f"   ✓ Saved interactive visualization to {html_path}")
        
        # Export topic terms
        print("   Extracting top terms per topic...")
        topic_terms = []
        for topic_id in range(best_num_topics):
            terms = best_model.show_topic(topic_id, topn=20)
            for term, weight in terms:
                topic_terms.append({
                    'topic_id': topic_id,
                    'term': term,
                    'weight': weight
                })
        
        terms_df = pd.DataFrame(topic_terms)
        terms_path = self.output_dir / "topic_terms.csv"
        terms_df.to_csv(terms_path, index=False)
        print(f"   ✓ Saved topic terms to {terms_path}")
        
        # Export document-topic distributions
        print("   Calculating document-topic distributions...")
        doc_topics = []
        for doc_id, doc_bow in enumerate(self.corpus):
            topic_dist = best_model.get_document_topics(doc_bow)
            for topic_id, probability in topic_dist:
                doc_topics.append({
                    'document_id': doc_id,
                    'ID': self.df.iloc[doc_id]['ID'],
                    'topic_id': topic_id,
                    'probability': probability
                })
        
        doc_topics_df = pd.DataFrame(doc_topics)
        doc_topics_path = self.output_dir / "document_topics.csv"
        doc_topics_df.to_csv(doc_topics_path, index=False)
        print(f"   ✓ Saved document topics to {doc_topics_path}")
        
        return best_model
    
    def print_topics(self, best_model, num_topics):
        """Print topics with top terms for manual review."""
        print(f"\n[7/7] Topic Summary ({num_topics} topics):")
        print("=" * 80)
        
        for topic_id in range(num_topics):
            print(f"\nTOPIC {topic_id}:")
            terms = best_model.show_topic(topic_id, topn=15)
            term_str = ', '.join([f"{term}({weight:.3f})" for term, weight in terms])
            print(f"   {term_str}")
            
            # Show sample documents for this topic
            doc_topics = best_model.get_document_topics(self.corpus)
            topic_docs = [(idx, topics) for idx, topics in enumerate(doc_topics)]
            # Sort by probability for this topic
            topic_docs_sorted = sorted(
                topic_docs,
                key=lambda x: next((p for t, p in x[1] if t == topic_id), 0),
                reverse=True
            )
            
            print(f"   Sample documents:")
            for idx, _ in topic_docs_sorted[:2]:
                title = self.df.iloc[idx]['TITLE'][:80]
                print(f"     - {title}...")
        
        print("\n" + "=" * 80)
    
    def run_analysis(self, topic_numbers=[5, 7, 10]):
        """Run the complete LDA analysis pipeline."""
        print("=" * 80)
        print("LDA TOPIC MODELING ANALYSIS")
        print("=" * 80)
        
        # Execute pipeline
        self.load_data()
        self.preprocess_corpus()
        self.build_bigrams()
        self.create_dictionary_corpus()
        best_num_topics = self.train_lda_models(topic_numbers)
        best_model = self.generate_visualizations(best_num_topics)
        self.print_topics(best_model, best_num_topics)
        
        print("\n" + "=" * 80)
        print("✓ ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"\nOutputs saved to: {self.output_dir}/")
        print(f"   - lda_visualization.html (open in browser)")
        print(f"   - coherence_scores.csv")
        print(f"   - topic_terms.csv")
        print(f"   - document_topics.csv")
        print(f"   - lda_model_*topics.pkl")
        print(f"   - dictionary.pkl")
        print("=" * 80)

def main():
    """Main entry point."""
    data_path = "topic_modeling/politics_hoax_text.csv"
    
    # Initialize analyzer
    analyzer = IndonesianLDAAnalyzer(data_path)
    
    # Run analysis with different topic numbers
    analyzer.run_analysis(topic_numbers=[5, 7, 10])

if __name__ == "__main__":
    main()
