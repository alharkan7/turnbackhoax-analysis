"""
Text Network Analysis for Political Hoaxes
Analyzes co-occurrence networks to reveal narrative structures in political hoax content
"""

import pandas as pd
import networkx as nx
import re
from collections import Counter, defaultdict
from itertools import combinations
import json
import os

# Indonesian stopwords
INDONESIAN_STOPWORDS = set([
    'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan', 'untuk', 
    'pada', 'adalah', 'oleh', 'karena', 'akan', 'telah', 'dapat', 'dalam',
    'ada', 'atau', 'juga', 'tidak', 'sudah', 'bisa', 'saat', 'tersebut',
    'video', 'foto', 'hoax', 'cek', 'fakta', 'beredar', 'viral', 'informasi',
    'berita', 'klaim', 'narasi', 'konten', 'bahwa', 'jika', 'sebagai', 'akan',
    'mereka', 'kita', 'kami', 'anda', 'saya', 'dia', 'beliau', 'pak', 'bu',
    'bapak', 'ibu', 'mas', 'mbak', 'saudara', 'tersebut', 'dimana', 'mana'
])

# Key political entities to track (case-insensitive patterns)
POLITICAL_ENTITIES = [
    'prabowo', 'gibran', 'anies', 'ganjar', 'mahfud', 'jokowi', 'cak imin',
    'muhaimin iskandar', 'kpu', 'bawaslu', 'mk', 'mahkamah konstitusi',
    'pdip', 'gerindra', 'nasdem', 'demokrat', 'pks', 'pan', 'golkar',
    'pemilu', 'pilpres', 'capres', 'cawapres', 'debat', 'kampanye',
    'koalisi', 'partai', 'tps', 'surat suara', 'sirekap', 'quick count',
    'johnny plate', 'sby', 'syahrul yasin limpo', 'bahlil', 'najwa shihab',
    'roy suryo', 'hak angket', 'curang', 'kecurangan'
]

def extract_narasi(content):
    """Extract NARASI section from content"""
    if pd.isna(content):
        return ""
    
    # Look for [NARASI] or Narasi: pattern
    narasi_pattern = r'\[NARASI\]:?\s*(.*?)(?:\[|===|$)'
    match = re.search(narasi_pattern, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    # Fallback: try without brackets
    narasi_pattern2 = r'NARASI:?\s*(.*?)(?:\[|===|$)'
    match = re.search(narasi_pattern2, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return ""

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove special characters but keep spaces and apostrophes
    text = re.sub(r'[^\w\s\']', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_entities(text, entity_list):
    """Extract predefined entities from text"""
    entities = []
    text_lower = text.lower()
    
    for entity in entity_list:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(entity.lower()) + r'\b'
        if re.search(pattern, text_lower):
            entities.append(entity)
    
    return entities

def extract_bigrams(text, min_freq=2):
    """Extract meaningful bigrams from text"""
    # Tokenize
    words = text.split()
    
    # Remove stopwords
    words = [w for w in words if w not in INDONESIAN_STOPWORDS and len(w) > 2]
    
    # Create bigrams
    bigrams = []
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        bigrams.append(bigram)
    
    return bigrams

def build_cooccurrence_network(df, min_cooccurrence=2):
    """Build co-occurrence network from documents"""
    print("Building co-occurrence network...")
    
    # Extract entities from all documents
    all_entities = []
    doc_entities = []
    
    for idx, row in df.iterrows():
        content = row.get('CONTENT', '')
        narasi = extract_narasi(content)
        
        if not narasi:
            # Fallback to TITLE if NARASI is empty
            narasi = row.get('TITLE', '')
        
        # Clean text
        cleaned = clean_text(narasi)
        
        # Extract entities
        entities = extract_entities(cleaned, POLITICAL_ENTITIES)
        
        if entities:
            doc_entities.append(entities)
            all_entities.extend(entities)
    
    print(f"Processed {len(doc_entities)} documents")
    print(f"Found {len(set(all_entities))} unique entities")
    
    # Build co-occurrence matrix
    cooccurrence = defaultdict(int)
    
    for entities in doc_entities:
        # Get unique entities in this document
        unique_entities = list(set(entities))
        
        # Create all pairs
        for e1, e2 in combinations(unique_entities, 2):
            # Sort to ensure consistent ordering
            pair = tuple(sorted([e1, e2]))
            cooccurrence[pair] += 1
    
    # Build network
    G = nx.Graph()
    
    # Add nodes
    entity_counts = Counter(all_entities)
    for entity, count in entity_counts.items():
        G.add_node(entity, count=count)
    
    # Add edges with weights
    for (e1, e2), weight in cooccurrence.items():
        if weight >= min_cooccurrence:
            G.add_edge(e1, e2, weight=weight)
    
    print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    return G, doc_entities, all_entities

def calculate_network_metrics(G):
    """Calculate various centrality metrics"""
    print("Calculating network metrics...")
    
    metrics = {}
    
    # Degree centrality
    degree_cent = nx.degree_centrality(G)
    metrics['degree_centrality'] = degree_cent
    
    # Betweenness centrality (bridge words)
    betweenness_cent = nx.betweenness_centrality(G)
    metrics['betweenness_centrality'] = betweenness_cent
    
    # Eigenvector centrality
    try:
        eigen_cent = nx.eigenvector_centrality(G, max_iter=1000)
        metrics['eigenvector_centrality'] = eigen_cent
    except:
        print("Could not calculate eigenvector centrality")
        metrics['eigenvector_centrality'] = {}
    
    # PageRank
    pagerank = nx.pagerank(G)
    metrics['pagerank'] = pagerank
    
    return metrics

def detect_communities(G):
    """Detect communities in the network"""
    print("Detecting communities...")
    
    # Use Louvain method for community detection
    from networkx.algorithms import community
    
    communities = community.greedy_modularity_communities(G)
    
    # Convert to dict
    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i
    
    return community_map, communities

def main():
    print("=" * 60)
    print("Text Network Analysis - Political Hoaxes")
    print("=" * 60)
    
    # Create output directory
    output_dir = "text_network/network_analysis_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv("Scraping turnbackhoax.id - Complete.csv")
    
    # Filter to 2024 and politics
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d %b %Y', errors='coerce')
    df_2024 = df[df['DATE'].dt.year == 2024].copy()
    df_politics = df_2024[df_2024['LLM Category'] == 'politics'].copy()
    
    print(f"Total rows: {len(df)}")
    print(f"2024 rows: {len(df_2024)}")
    print(f"Politics rows: {len(df_politics)}")
    
    # Build network
    G, doc_entities, all_entities = build_cooccurrence_network(df_politics, min_cooccurrence=2)
    
    # Calculate metrics
    metrics = calculate_network_metrics(G)
    
    # Detect communities
    community_map, communities = detect_communities(G)
    
    # Save results
    print("\nSaving results...")
    
    # 1. Top entities by different metrics
    results = []
    for node in G.nodes():
        results.append({
            'entity': node,
            'count': G.nodes[node]['count'],
            'degree_centrality': metrics['degree_centrality'].get(node, 0),
            'betweenness_centrality': metrics['betweenness_centrality'].get(node, 0),
            'eigenvector_centrality': metrics['eigenvector_centrality'].get(node, 0),
            'pagerank': metrics['pagerank'].get(node, 0),
            'community': community_map.get(node, -1)
        })
    
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('betweenness_centrality', ascending=False)
    results_df.to_csv(f"{output_dir}/top_entities.csv", index=False)
    print(f"Saved: {output_dir}/top_entities.csv")
    
    # 2. Bridge words (high betweenness centrality)
    bridge_df = results_df.nlargest(20, 'betweenness_centrality')
    bridge_df.to_csv(f"{output_dir}/bridge_words.csv", index=False)
    print(f"Saved: {output_dir}/bridge_words.csv")
    
    # 3. Communities
    community_data = []
    for i, comm in enumerate(communities):
        community_data.append({
            'community_id': i,
            'size': len(comm),
            'entities': ', '.join(sorted(comm))
        })
    
    community_df = pd.DataFrame(community_data)
    community_df.to_csv(f"{output_dir}/communities.csv", index=False)
    print(f"Saved: {output_dir}/communities.csv")
    
    # 4. Network statistics
    stats = {
        'total_documents': len(df_politics),
        'unique_entities': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'network_density': nx.density(G),
        'num_communities': len(communities),
        'avg_clustering': nx.average_clustering(G)
    }
    
    with open(f"{output_dir}/network_stats.txt", 'w') as f:
        f.write("Network Statistics\n")
        f.write("=" * 50 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    print(f"Saved: {output_dir}/network_stats.txt")
    
    # 5. Save graph for visualization
    import pickle
    with open(f"{output_dir}/network_graph.pkl", 'wb') as f:
        pickle.dump(G, f)
    print(f"Saved: {output_dir}/network_graph.pkl")
    
    # Save metadata for visualization
    metadata = {
        'metrics': {k: {node: float(v) for node, v in metric.items()} 
                   for k, metric in metrics.items()},
        'community_map': community_map,
        'stats': stats
    }
    
    with open(f"{output_dir}/network_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved: {output_dir}/network_metadata.json")
    
    # Print summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Documents analyzed: {len(df_politics)}")
    print(f"Unique entities: {G.number_of_nodes()}")
    print(f"Connections (edges): {G.number_of_edges()}")
    print(f"Communities detected: {len(communities)}")
    print(f"\nTop 10 entities by betweenness centrality (bridge words):")
    print(bridge_df[['entity', 'betweenness_centrality', 'count']].head(10).to_string(index=False))
    
    print("\n✓ Analysis complete! Results saved to:", output_dir)

if __name__ == "__main__":
    main()
