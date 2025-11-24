"""
Multi-Category Text Network Analysis
Analyzes co-occurrence networks for politics, scam, and others categories
"""

import pandas as pd
import networkx as nx
import re
from collections import Counter, defaultdict
from itertools import combinations
import json
import os
import pickle

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

# Category-specific entities
ENTITY_LISTS = {
    'politics': [
        'prabowo', 'gibran', 'anies', 'ganjar', 'mahfud', 'jokowi', 'cak imin',
        'muhaimin iskandar', 'kpu', 'bawaslu', 'mk', 'mahkamah konstitusi',
        'pdip', 'gerindra', 'nasdem', 'demokrat', 'pks', 'pan', 'golkar',
        'pemilu', 'pilpres', 'capres', 'cawapres', 'debat', 'kampanye',
        'koalisi', 'partai', 'tps', 'surat suara', 'sirekap', 'quick count',
        'johnny plate', 'sby', 'syahrul yasin limpo', 'bahlil', 'najwa shihab',
        'roy suryo', 'hak angket', 'curang', 'kecurangan'
    ],
    'scam': [
        'bank', 'bri', 'bni', 'mandiri', 'bca', 'rekening', 'transfer',
        'undian', 'hadiah', 'giveaway', 'saldo', 'dana', 'gopay', 'ovo',
        'pulsa', 'kuota', 'internet gratis', 'lowongan', 'loker', 'rekrutmen',
        'cpns', 'bumn', 'pln', 'pertamina', 'bpjs', 'bansos', 'blt',
        'prakerja', 'kartu', 'promo', 'gratis', 'penipuan', 'penipu',
        'akun palsu', 'modus', 'whatsapp', 'facebook', 'instagram', 'tiktok'
    ],
    'others': [
        'covid', 'vaksin', 'omicron', 'virus', 'pandemi', 'kesehatan',
        'who', 'kemenkes', 'rs', 'rumah sakit', 'obat', 'ivermectin',
        'gempa', 'tsunami', 'banjir', 'longsor', 'bencana', 'bmkg',
        'gunung', 'erupsi', 'palestina', 'israel', 'gaza', 'hamas',
        'ukraina', 'rusia', 'perang', 'china', 'amerika', 'as'
    ]
}

def extract_narasi(content):
    """Extract NARASI section from content"""
    if pd.isna(content):
        return ""
    
    narasi_pattern = r'\[NARASI\]:?\s*(.*?)(?:\[|===|$)'
    match = re.search(narasi_pattern, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    narasi_pattern2 = r'NARASI:?\s*(.*?)(?:\[|===|$)'
    match = re.search(narasi_pattern2, content, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return ""

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[^\w\s\']', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_entities(text, entity_list):
    """Extract predefined entities from text"""
    entities = []
    text_lower = text.lower()
    
    for entity in entity_list:
        pattern = r'\b' + re.escape(entity.lower()) + r'\b'
        if re.search(pattern, text_lower):
            entities.append(entity)
    
    return entities

def build_cooccurrence_network(df, entity_list, min_cooccurrence=2):
    """Build co-occurrence network from documents"""
    
    all_entities = []
    doc_entities = []
    
    for idx, row in df.iterrows():
        content = row.get('CONTENT', '')
        narasi = extract_narasi(content)
        
        if not narasi:
            narasi = row.get('TITLE', '')
        
        cleaned = clean_text(narasi)
        entities = extract_entities(cleaned, entity_list)
        
        if entities:
            doc_entities.append(entities)
            all_entities.extend(entities)
    
    # Build co-occurrence matrix
    cooccurrence = defaultdict(int)
    
    for entities in doc_entities:
        unique_entities = list(set(entities))
        
        for e1, e2 in combinations(unique_entities, 2):
            pair = tuple(sorted([e1, e2]))
            cooccurrence[pair] += 1
    
    # Build network
    G = nx.Graph()
    
    entity_counts = Counter(all_entities)
    for entity, count in entity_counts.items():
        G.add_node(entity, count=count)
    
    for (e1, e2), weight in cooccurrence.items():
        if weight >= min_cooccurrence:
            G.add_edge(e1, e2, weight=weight)
    
    return G, len(doc_entities), len(all_entities)

def calculate_network_metrics(G):
    """Calculate various centrality metrics"""
    
    metrics = {}
    
    degree_cent = nx.degree_centrality(G)
    metrics['degree_centrality'] = degree_cent
    
    betweenness_cent = nx.betweenness_centrality(G)
    metrics['betweenness_centrality'] = betweenness_cent
    
    try:
        eigen_cent = nx.eigenvector_centrality(G, max_iter=1000)
        metrics['eigenvector_centrality'] = eigen_cent
    except:
        metrics['eigenvector_centrality'] = {}
    
    pagerank = nx.pagerank(G)
    metrics['pagerank'] = pagerank
    
    return metrics

def detect_communities(G):
    """Detect communities in the network"""
    from networkx.algorithms import community
    
    communities = community.greedy_modularity_communities(G)
    
    community_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i
    
    return community_map, communities

def analyze_category(df, category, entity_list, output_dir):
    """Analyze a single category"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {category.upper()}")
    print('='*60)
    
    # Build network
    G, num_docs, total_entities = build_cooccurrence_network(df, entity_list, min_cooccurrence=2)
    
    print(f"Documents with entities: {num_docs}")
    print(f"Unique entities: {G.number_of_nodes()}")
    print(f"Connections: {G.number_of_edges()}")
    
    if G.number_of_nodes() == 0:
        print(f"⚠️  No entities found for {category}")
        return None
    
    # Calculate metrics
    metrics = calculate_network_metrics(G)
    
    # Detect communities
    community_map, communities = detect_communities(G)
    
    # Prepare results
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
    
    # Save results
    category_dir = f"{output_dir}/{category}"
    os.makedirs(category_dir, exist_ok=True)
    
    results_df.to_csv(f"{category_dir}/top_entities.csv", index=False)
    
    # Save graph
    with open(f"{category_dir}/network_graph.pkl", 'wb') as f:
        pickle.dump(G, f)
    
    # Save metadata
    metadata = {
        'metrics': {k: {node: float(v) for node, v in metric.items()} 
                   for k, metric in metrics.items()},
        'community_map': community_map,
        'stats': {
            'total_documents': len(df),
            'documents_with_entities': num_docs,
            'unique_entities': G.number_of_nodes(),
            'total_edges': G.number_of_edges(),
            'network_density': nx.density(G) if G.number_of_nodes() > 1 else 0,
            'num_communities': len(communities)
        }
    }
    
    with open(f"{category_dir}/network_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✓ Saved results to: {category_dir}")
    
    return {
        'graph': G,
        'metadata': metadata,
        'results_df': results_df,
        'category': category
    }

def main():
    print("=" * 60)
    print("Multi-Category Text Network Analysis")
    print("=" * 60)
    
    # Create output directory
    output_dir = "text_network/network_analysis_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    print("\nLoading data...")
    df = pd.read_csv("Scraping turnbackhoax.id - Complete.csv")
    
    # Filter to 2024
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d %b %Y', errors='coerce')
    df_2024 = df[df['DATE'].dt.year == 2024].copy()
    
    print(f"Total 2024 rows: {len(df_2024)}")
    
    # Analyze each category
    results = {}
    
    for category in ['politics', 'scam', 'others']:
        df_category = df_2024[df_2024['LLM Category'] == category].copy()
        print(f"\n{category.upper()}: {len(df_category)} documents")
        
        if len(df_category) > 0:
            result = analyze_category(
                df_category, 
                category, 
                ENTITY_LISTS[category],
                output_dir
            )
            if result:
                results[category] = result
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    
    for category, result in results.items():
        stats = result['metadata']['stats']
        print(f"\n{category.upper()}:")
        print(f"  Entities: {stats['unique_entities']}")
        print(f"  Edges: {stats['total_edges']}")
        print(f"  Communities: {stats['num_communities']}")

if __name__ == "__main__":
    main()
