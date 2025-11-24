"""
Create Tabbed Multi-Category Network Visualization
Generates a single HTML with tabs for politics, scam, and others networks
"""

import pickle
import json
import os

def load_category_data(category, base_dir):
    """Load network data for a category"""
    category_dir = f"{base_dir}/{category}"
    
    with open(f"{category_dir}/network_graph.pkl", 'rb') as f:
        G = pickle.load(f)
    
    with open(f"{category_dir}/network_metadata.json", 'r') as f:
        metadata = json.load(f)
    
    return G, metadata

def prepare_network_data(G, metadata):
    """Prepare node and edge data for vis.js"""
    betweenness = metadata['metrics']['betweenness_centrality']
    degree_cent = metadata['metrics']['degree_centrality']
    community_map = metadata['community_map']
    
    colors = {
        0: '#e74c3c', 1: '#3498db', 2: '#2ecc71', 
        3: '#f39c12', 4: '#9b59b6', 5: '#1abc9c',
        6: '#e67e22', 7: '#34495e'
    }
    
    nodes_data = []
    for node in G.nodes():
        count = G.nodes[node]['count']
        bet_cent = betweenness.get(node, 0)
        deg_cent = degree_cent.get(node, 0)
        community = community_map.get(node, 0)
        
        nodes_data.append({
            'id': node,
            'label': node,
            'count': count,
            'betweenness': bet_cent,
            'degree': deg_cent,
            'community': community,
            'color': colors.get(community, '#95a5a6')
        })
    
    edges_data = []
    for e1, e2, data in G.edges(data=True):
        weight = data['weight']
        edges_data.append({
            'from': e1,
            'to': e2,
            'value': weight
        })
    
    return nodes_data, edges_data

def generate_tabbed_html(categories_data, output_path):
    """Generate HTML with tabs for multiple categories"""
    
    # Prepare data for all categories
    network_datasets = {}
    for category, (G, metadata) in categories_data.items():
        nodes, edges = prepare_network_data(G, metadata)
        network_datasets[category] = {
            'nodes': nodes,
            'edges': edges,
            'stats': metadata['stats']
        }
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Turnbackhoax Text Network Analysis</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            overflow: hidden;
            background: #f8f9fa;
        }}
        
        #header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        #header h1 {{
            font-size: 20px;
            font-weight: 600;
        }}
        
        .tabs {{
            display: flex;
            background: white;
            border-bottom: 2px solid #dee2e6;
            padding: 0 20px;
        }}
        
        .tab {{
            padding: 12px 24px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            font-weight: 500;
            color: #6c757d;
        }}
        
        .tab:hover {{
            background: #f8f9fa;
            color: #495057;
        }}
        
        .tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
        }}
        
        .tab-label {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .tab-badge {{
            background: #e9ecef;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        }}
        
        .tab.active .tab-badge {{
            background: #667eea;
            color: white;
        }}
        
        #container {{
            display: flex;
            height: calc(100vh - 115px);
        }}
        
        #controls {{
            width: 320px;
            background: #f8f9fa;
            border-right: 1px solid #dee2e6;
            overflow-y: auto;
            padding: 20px;
        }}
        
        .tab-content {{
            flex: 1;
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .network-canvas {{
            width: 100%;
            height: 100%;
            background: white;
        }}
        
        .control-section {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .control-section h3 {{
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .control-group {{
            margin-bottom: 12px;
        }}
        
        .control-group label {{
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #495057;
            margin-bottom: 5px;
        }}
        
        .control-group input[type="range"] {{
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #e9ecef;
            outline: none;
            -webkit-appearance: none;
        }}
        
        .control-group input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }}
        
        .control-group select {{
            width: 100%;
            padding: 8px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-size: 12px;
            background: white;
        }}
        
        .value-display {{
            float: right;
            font-size: 12px;
            font-weight: 600;
            color: #667eea;
        }}
        
        button {{
            width: 100%;
            padding: 10px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 5px;
            transition: background 0.2s;
        }}
        
        button:hover {{
            background: #5568d3;
        }}
        
        button.secondary {{
            background: #6c757d;
        }}
        
        button.secondary:hover {{
            background: #5a6268;
        }}
        
        .stats {{
            font-size: 11px;
            color: #6c757d;
            margin-top: 10px;
        }}
        
        #info-panel {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            max-width: 300px;
            display: none;
            z-index: 100;
        }}
        
        #info-panel h4 {{
            font-size: 14px;
            margin-bottom: 8px;
        }}
        
        #info-panel .info-row {{
            font-size: 12px;
            margin-bottom: 4px;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🕸️ Turnbackhoax Text Network Analysis</h1>
    </div>
    
    <div class="tabs">
        <div class="tab active" onclick="switchTab('politics')">
            <div class="tab-label">
                <span>Politics</span>
                <span class="tab-badge">{network_datasets['politics']['stats']['unique_entities']} entities</span>
            </div>
        </div>
        <div class="tab" onclick="switchTab('scam')">
            <div class="tab-label">
                <span>Scam</span>
                <span class="tab-badge">{network_datasets['scam']['stats']['unique_entities']} entities</span>
            </div>
        </div>
        <div class="tab" onclick="switchTab('others')">
            <div class="tab-label">
                <span>Others</span>
                <span class="tab-badge">{network_datasets['others']['stats']['unique_entities']} entities</span>
            </div>
        </div>
    </div>
    
    <div id="container">
        <div id="controls">
            <div class="control-section">
                <h3>⚙️ Physics Settings</h3>
                
                <div class="control-group">
                    <label>Solver Algorithm</label>
                    <select id="solver">
                        <option value="barnesHut">Barnes-Hut (Fast)</option>
                        <option value="forceAtlas2Based" selected>Force Atlas 2 (Balanced)</option>
                        <option value="repulsion">Repulsion (Spread)</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label>Spring Length <span class="value-display" id="spring-val">150</span></label>
                    <input type="range" id="springLength" min="50" max="500" value="150">
                </div>
                
                <div class="control-group">
                    <label>Repulsion <span class="value-display" id="repulsion-val">-2000</span></label>
                    <input type="range" id="gravitationalConstant" min="-10000" max="-500" step="100" value="-2000">
                </div>
            </div>
            
            <div class="control-section">
                <h3>🎨 Display Options</h3>
                
                <div class="control-group">
                    <label>Node Size By</label>
                    <select id="nodeSizing">
                        <option value="count">Mention Count</option>
                        <option value="betweenness">Betweenness Centrality</option>
                        <option value="uniform">Uniform</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label>Min Node Size <span class="value-display" id="min-size-val">10</span></label>
                    <input type="range" id="minNodeSize" min="5" max="30" value="10">
                </div>
            </div>
            
            <button onclick="updateNetwork()">🔄 Apply Changes</button>
            <button onclick="togglePhysics()" id="physics-toggle">⏸️ Pause Physics</button>
            <button onclick="fitNetwork()" class="secondary">⊡ Fit to Screen</button>
            
            <div class="control-section">
                <h3>📊 Statistics</h3>
                <div class="stats" id="current-stats"></div>
            </div>
        </div>
        
        <div id="politics-content" class="tab-content active">
            <div id="network-politics" class="network-canvas"></div>
        </div>
        <div id="scam-content" class="tab-content">
            <div id="network-scam" class="network-canvas"></div>
        </div>
        <div id="others-content" class="tab-content">
            <div id="network-others" class="network-canvas"></div>
        </div>
    </div>
    
    <div id="info-panel">
        <h4 id="info-title"></h4>
        <div id="info-content"></div>
    </div>

    <script>
        const networkData = {json.dumps(network_datasets, indent=4)};
        
        let networks = {{}};
        let currentCategory = 'politics';
        
        function initAllNetworks() {{
            const options = {{
                nodes: {{
                    shape: 'dot',
                    font: {{ size: 14, face: 'Arial' }},
                    borderWidth: 2
                }},
                edges: {{
                    smooth: {{ type: 'continuous' }},
                    color: {{ color: '#cccccc', highlight: '#667eea' }}
                }},
                physics: {{
                    enabled: true,
                    forceAtlas2Based: {{
                        gravitationalConstant: -2000,
                        centralGravity: 0.01,
                        springLength: 150,
                        springConstant: 0.05,
                        damping: 0.4,
                        avoidOverlap: 0.5
                    }},
                    solver: 'forceAtlas2Based',
                    stabilization: {{
                        enabled: true,
                        iterations: 1500,
                        updateInterval: 50,
                        fit: true
                    }}
                }},
                interaction: {{
                    hover: true,
                    navigationButtons: true
                }}
            }};
            
            ['politics', 'scam', 'others'].forEach(category => {{
                const container = document.getElementById('network-' + category);
                const data = prepareNetworkData(category);
                networks[category] = new vis.Network(container, data, options);
                
                networks[category].once("stabilizationIterationsDone", function() {{
                    networks[category].setOptions({{ physics: false }});
                    console.log(category + " stabilized");
                    if (category === currentCategory) {{
                        updatePhysicsButton(false);
                    }}
                }});
                
                networks[category].on("click", function(params) {{
                    if (params.nodes.length > 0) {{
                        showNodeInfo(params.nodes[0], category);
                    }}
                }});
            }});
            
            updateStats();
        }}
        
        function prepareNetworkData(category) {{
            const data = networkData[category];
            const nodes = data.nodes.map(node => ({{
                id: node.id,
                label: node.label,
                size: 10 + (node.count * 1.5),
                color: node.color,
                title: `${{node.label}}\\nMentions: ${{node.count}}\\nBetweenness: ${{node.betweenness.toFixed(3)}}`,
                ...node
            }}));
            
            const edges = data.edges.map(edge => ({{
                from: edge.from,
                to: edge.to,
                width: edge.value
            }}));
            
            return {{
                nodes: new vis.DataSet(nodes),
                edges: new vis.DataSet(edges)
            }};
        }}
        
        function switchTab(category) {{
            currentCategory = category;
            
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.closest('.tab').classList.add('active');
            document.getElementById(category + '-content').classList.add('active');
            
            updateStats();
            updatePhysicsButton(networks[category].physics.physicsEnabled);
        }}
        
        function updateNetwork() {{
            const nodeSizing = document.getElementById('nodeSizing').value;
            const minSize = parseInt(document.getElementById('minNodeSize').value);
            
            const data = networkData[currentCategory];
            const nodes = data.nodes.map(node => {{
                let size;
                if (nodeSizing === 'count') {{
                    size = minSize + (node.count * 1.5);
                }} else if (nodeSizing === 'betweenness') {{
                    size = minSize + (node.betweenness * 200);
                }} else {{
                    size = 20;
                }}
                
                return {{
                    id: node.id,
                    label: node.label,
                    size: Math.max(size, minSize),
                    color: node.color,
                    title: `${{node.label}}\\nMentions: ${{node.count}}\\nBetweenness: ${{node.betweenness.toFixed(3)}}`,
                    ...node
                }};
            }});
            
            networks[currentCategory].setData({{
                nodes: new vis.DataSet(nodes),
                edges: networks[currentCategory].body.data.edges
            }});
            
            updatePhysics();
        }}
        
        function updatePhysics() {{
            const solver = document.getElementById('solver').value;
            const springLength = parseInt(document.getElementById('springLength').value);
            const gravitationalConstant = parseInt(document.getElementById('gravitationalConstant').value);
            
            let physicsOptions = {{ enabled: true, solver: solver }};
            
            if (solver === 'forceAtlas2Based') {{
                physicsOptions.forceAtlas2Based = {{
                    gravitationalConstant: gravitationalConstant,
                    springLength: springLength,
                    springConstant: 0.05,
                    damping: 0.4,
                    avoidOverlap: 0.5
                }};
            }} else if (solver === 'barnesHut') {{
                physicsOptions.barnesHut = {{
                    gravitationalConstant: gravitationalConstant,
                    springLength: springLength,
                    springConstant: 0.05,
                    damping: 0.09,
                    avoidOverlap: 0.5
                }};
            }}
            
            networks[currentCategory].setOptions({{ physics: physicsOptions }});
        }}
        
        function togglePhysics() {{
            const enabled = networks[currentCategory].physics.physicsEnabled;
            networks[currentCategory].setOptions({{ physics: !enabled }});
            updatePhysicsButton(!enabled);
        }}
        
        function updatePhysicsButton(enabled) {{
            const button = document.getElementById('physics-toggle');
            button.textContent = enabled ? '⏸️ Pause Physics' : '▶️ Resume Physics';
            button.style.background = enabled ? '#667eea' : '#2ecc71';
        }}
        
        function fitNetwork() {{
            networks[currentCategory].fit({{ animation: {{ duration: 1000 }} }});
        }}
        
        function showNodeInfo(nodeId, category) {{
            const node = networkData[category].nodes.find(n => n.id === nodeId);
            if (!node) return;
            
            document.getElementById('info-title').textContent = node.label;
            document.getElementById('info-content').innerHTML = `
                <div class="info-row"><b>Mentions:</b> ${{node.count}}</div>
                <div class="info-row"><b>Betweenness:</b> ${{node.betweenness.toFixed(4)}}</div>
                <div class="info-row"><b>Degree:</b> ${{node.degree.toFixed(4)}}</div>
                <div class="info-row"><b>Community:</b> ${{node.community}}</div>
            `;
            document.getElementById('info-panel').style.display = 'block';
        }}
        
        function updateStats() {{
            const stats = networkData[currentCategory].stats;
            document.getElementById('current-stats').innerHTML = `
                <div><b>Documents:</b> ${{stats.total_documents}}</div>
                <div><b>With Entities:</b> ${{stats.documents_with_entities}}</div>
                <div><b>Unique Entities:</b> ${{stats.unique_entities}}</div>
                <div><b>Connections:</b> ${{stats.total_edges}}</div>
                <div><b>Communities:</b> ${{stats.num_communities}}</div>
                <div><b>Density:</b> ${{stats.network_density.toFixed(3)}}</div>
            `;
        }}
        
        // Range displays
        document.getElementById('springLength').oninput = function() {{
            document.getElementById('spring-val').textContent = this.value;
        }};
        document.getElementById('gravitationalConstant').oninput = function() {{
            document.getElementById('repulsion-val').textContent = this.value;
        }};
        document.getElementById('minNodeSize').oninput = function() {{
            document.getElementById('min-size-val').textContent = this.value;
        }};
        
        // Initialize
        initAllNetworks();
    </script>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    print("=" * 60)
    print("Creating Tabbed Multi-Category Visualization")
    print("=" * 60)
    
    base_dir = "text_network/network_analysis_results"
    
    # Load data for all categories
    categories_data = {}
    for category in ['politics', 'scam', 'others']:
        print(f"\nLoading {category} data...")
        G, metadata = load_category_data(category, base_dir)
        categories_data[category] = (G, metadata)
        print(f"  ✓ {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Generate HTML
    print("\nGenerating tabbed HTML...")
    output_path = f"{base_dir}/multi_category_network.html"
    generate_tabbed_html(categories_data, output_path)
    
    print(f"\n✓ Created: {output_path}")
    print("\nOpen this file in your browser to view all three networks!")

if __name__ == "__main__":
    main()
