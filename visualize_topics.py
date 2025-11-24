#!/usr/bin/env python3
"""
Create supplementary visualizations for LDA topic modeling results.
Generates bar charts, heatmaps, and word clouds for topic interpretation.

Usage:
    python3 visualize_topics.py <output_dir>
    
    output_dir: directory containing LDA results (e.g., topic_modeling/scam_category)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from pathlib import Path
import sys

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class TopicVisualizer:
    """Creates visualizations for LDA topic modeling results."""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.viz_dir = self.output_dir / "visualizations"
        self.viz_dir.mkdir(exist_ok=True)
        
        # Load data
        self.topic_terms = pd.read_csv(self.output_dir / "topic_terms.csv")
        self.doc_topics = pd.read_csv(self.output_dir / "document_topics.csv")
        self.coherence = pd.read_csv(self.output_dir / "coherence_scores.csv")
        
        # Get number of topics from best model
        self.num_topics = self.coherence.loc[self.coherence['coherence_score'].idxmax(), 'num_topics']
        self.num_topics = int(self.num_topics)
        
    def plot_coherence_scores(self):
        """Plot coherence scores comparison."""
        print("\n[1/5] Plotting coherence scores...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(self.coherence['num_topics'], self.coherence['coherence_score'], 
                marker='o', linewidth=2, markersize=10, color='#2E86AB')
        ax.set_xlabel('Number of Topics', fontsize=12, fontweight='bold')
        ax.set_ylabel('Coherence Score (C_v)', fontsize=12, fontweight='bold')
        ax.set_title('LDA Model Coherence Comparison', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        
        # Highlight best score
        best_idx = self.coherence['coherence_score'].idxmax()
        best_topics = self.coherence.loc[best_idx, 'num_topics']
        best_score = self.coherence.loc[best_idx, 'coherence_score']
        ax.scatter([best_topics], [best_score], color='#A23B72', s=200, zorder=5, 
                  label=f'Best: {int(best_topics)} topics ({best_score:.4f})')
        ax.legend(fontsize=11)
        
        plt.tight_layout()
        save_path = self.viz_dir / "coherence_comparison.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved to {save_path}")
    
    def plot_top_terms_per_topic(self, top_n=15):
        """Plot top terms for each topic as horizontal bar charts."""
        print(f"\n[2/5] Plotting top {top_n} terms per topic...")
        
        # Create subplot grid
        ncols = 2
        nrows = (self.num_topics + 1) // 2
        
        fig, axes = plt.subplots(nrows, ncols, figsize=(16, 4 * nrows))
        axes = axes.flatten() if self.num_topics > 1 else [axes]
        
        for topic_id in range(self.num_topics):
            ax = axes[topic_id]
            
            # Get top terms for this topic
            topic_data = self.topic_terms[self.topic_terms['topic_id'] == topic_id].nlargest(top_n, 'weight')
            
            # Plot horizontal bar chart
            y_pos = np.arange(len(topic_data))
            ax.barh(y_pos, topic_data['weight'], color=f'C{topic_id % 10}', alpha=0.7)
            ax.set_yticks(y_pos)
            ax.set_yticklabels(topic_data['term'], fontsize=9)
            ax.invert_yaxis()
            ax.set_xlabel('Weight', fontsize=10)
            ax.set_title(f'Topic {topic_id}', fontsize=11, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
        
        # Hide unused subplots
        for idx in range(self.num_topics, len(axes)):
            axes[idx].axis('off')
        
        plt.suptitle(f'Top {top_n} Terms per Topic', fontsize=14, fontweight='bold', y=1.002)
        plt.tight_layout()
        
        save_path = self.viz_dir / "top_terms_per_topic.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved to {save_path}")
    
    def plot_topic_distribution_heatmap(self):
        """Plot heatmap of topic distributions across documents."""
        print("\n[3/5] Creating topic distribution heatmap...")
        
        # Get dominant topic for each document
        dominant_topics = self.doc_topics.loc[
            self.doc_topics.groupby('document_id')['probability'].idxmax()
        ]
        
        # Count documents per topic
        topic_counts = dominant_topics['topic_id'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar chart
        bars = ax.bar(topic_counts.index, topic_counts.values, 
                      color=[f'C{i % 10}' for i in range(len(topic_counts))], 
                      alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Topic ID', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Documents', fontsize=12, fontweight='bold')
        ax.set_title('Document Distribution Across Topics (Dominant Topic Assignment)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(self.num_topics))
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        save_path = self.viz_dir / "topic_distribution.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved to {save_path}")
    
    def create_word_clouds(self, top_n=50):
        """Create word clouds for each topic."""
        print(f"\n[4/5] Generating word clouds for topics...")
        
        # Create grid for word clouds
        ncols = 3
        nrows = (self.num_topics + 2) // 3
        
        fig, axes = plt.subplots(nrows, ncols, figsize=(15, 5 * nrows))
        axes = axes.flatten() if self.num_topics > 1 else [axes]
        
        for topic_id in range(self.num_topics):
            ax = axes[topic_id]
            
            # Get terms and weights for this topic
            topic_data = self.topic_terms[self.topic_terms['topic_id'] == topic_id].nlargest(top_n, 'weight')
            
            # Create word frequency dict
            word_freq = dict(zip(topic_data['term'], topic_data['weight']))
            
            # Generate word cloud
            wc = WordCloud(width=800, height=400, 
                          background_color='white',
                          colormap=f'tab10',
                          relative_scaling=0.5,
                          min_font_size=10).generate_from_frequencies(word_freq)
            
            ax.imshow(wc, interpolation='bilinear')
            ax.set_title(f'Topic {topic_id}', fontsize=12, fontweight='bold')
            ax.axis('off')
        
        # Hide unused subplots
        for idx in range(self.num_topics, len(axes)):
            axes[idx].axis('off')
        
        plt.suptitle('Word Clouds per Topic', fontsize=14, fontweight='bold', y=1.002)
        plt.tight_layout()
        
        save_path = self.viz_dir / "wordclouds.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved to {save_path}")
    
    def create_topic_summary_table(self):
        """Create a summary table of topics with top terms."""
        print("\n[5/5] Creating topic summary table...")
        
        summary_data = []
        
        for topic_id in range(self.num_topics):
            # Get top 10 terms
            topic_data = self.topic_terms[self.topic_terms['topic_id'] == topic_id].nlargest(10, 'weight')
            top_terms = ', '.join(topic_data['term'].tolist())
            
            # Count documents
            doc_count = len(self.doc_topics[
                (self.doc_topics['topic_id'] == topic_id) & 
                (self.doc_topics['probability'] > 0.3)
            ]['document_id'].unique())
            
            summary_data.append({
                'Topic ID': topic_id,
                'Top 10 Terms': top_terms,
                'Document Count (>30% prob)': doc_count
            })
        
        summary_df = pd.DataFrame(summary_data)
        save_path = self.output_dir / "topic_summary.csv"
        summary_df.to_csv(save_path, index=False)
        print(f"   ✓ Saved to {save_path}")
        
        return summary_df
    
    def run_all_visualizations(self):
        """Generate all visualizations."""
        print("=" * 60)
        print("CREATING TOPIC VISUALIZATIONS")
        print("=" * 60)
        print(f"\nUsing best model: {self.num_topics} topics")
        
        self.plot_coherence_scores()
        self.plot_top_terms_per_topic()
        self.plot_topic_distribution_heatmap()
        self.create_word_clouds()
        summary_df = self.create_topic_summary_table()
        
        print("\n" + "=" * 60)
        print("✓ VISUALIZATIONS COMPLETE")
        print("=" * 60)
        print(f"\nAll visualizations saved to: {self.viz_dir}/")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 visualize_topics.py <output_dir>")
        print("  output_dir: directory containing LDA results")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    visualizer = TopicVisualizer(output_dir)
    visualizer.run_all_visualizations()

if __name__ == "__main__":
    main()
