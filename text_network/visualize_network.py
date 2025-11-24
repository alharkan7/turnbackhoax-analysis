"""
Enhanced Interactive Network Visualization with Control Panel
Creates a readable network graph with adjustable layout settings
"""

import pickle
import json
import pandas as pd
import networkx as nx

def create_enhanced_network_html(graph_path, metadata_path, output_path):
    """Create enhanced network visualization with control panel"""
    
    # Load graph and metadata
    with open(graph_path, 'rb') as f:
        G = pickle.load(f)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    print(f"Loaded graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Get metrics
    betweenness = metadata['metrics']['betweenness_centrality']
    degree_cent = metadata['metrics']['degree_centrality']
    community_map = metadata['community_map']
    
    # Define colors for communities
    colors = {
        0: '#e74c3c',  # Red - Government
        1: '#3498db',  # Blue - Electoral Process
        2: '#2ecc71',  # Green - Fraud & Oversight
        3: '#f39c12',  # Orange - Opposition
        4: '#9b59b6'   # Purple - Media Critics
    }
    
    # Prepare node data
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
    
    # Prepare edge data
    edges_data = []
    for e1, e2, data in G.edges(data=True):
        weight = data['weight']
        edges_data.append({
            'from': e1,
            'to': e2,
            'value': weight
        })
    
    # Create HTML with vis.js
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Political Hoax Network Analysis</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            overflow: hidden;
        }
        
        #header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
            z-index: 10;
        }
        
        #header h1 {
            font-size: 20px;
            font-weight: 600;
        }
        
        #header p {
            font-size: 13px;
            opacity: 0.9;
            margin-top: 3px;
        }
        
        #container {
            display: flex;
            height: calc(100vh - 65px);
        }
        
        #controls {
            width: 320px;
            background: #f8f9fa;
            border-right: 1px solid #dee2e6;
            overflow-y: auto;
            padding: 20px;
        }
        
        #mynetwork {
            flex: 1;
            background: #ffffff;
        }
        
        .control-section {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .control-section h3 {
            font-size: 14px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .control-group {
            margin-bottom: 12px;
        }
        
        .control-group label {
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: #495057;
            margin-bottom: 5px;
        }
        
        .control-group input[type="range"] {
            width: 100%;
            height: 6px;
            border-radius: 3px;
            background: #e9ecef;
            outline: none;
            -webkit-appearance: none;
        }
        
        .control-group input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }
        
        .control-group input[type="range"]::-moz-range-thumb {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }
        
        .value-display {
            display: inline-block;
            float: right;
            font-size: 12px;
            font-weight: 600;
            color: #667eea;
        }
        
        .control-group select {
            width: 100%;
            padding: 8px;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-size: 12px;
            background: white;
        }
        
        button {
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
        }
        
        button:hover {
            background: #5568d3;
        }
        
        button.secondary {
            background: #6c757d;
        }
        
        button.secondary:hover {
            background: #5a6268;
        }
        
        .legend {
            margin-top: 15px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 12px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .stats {
            font-size: 11px;
            color: #6c757d;
            margin-top: 10px;
        }
        
        .stats div {
            margin-bottom: 3px;
        }
        
        #info-panel {
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
        }
        
        #info-panel h4 {
            font-size: 14px;
            margin-bottom: 8px;
            color: #2c3e50;
        }
        
        #info-panel .info-row {
            font-size: 12px;
            margin-bottom: 4px;
            color: #495057;
        }
        
        #info-panel .info-label {
            font-weight: 600;
            display: inline-block;
            width: 120px;
        }
    </style>
</head>
<body>
    <div id="header">
        <h1>🕸️ Political Hoax Network Analysis</h1>
        <p>38 entities • 227 connections • 5 communities | 2024 Indonesian Political Hoaxes</p>
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
                    <label>Spring Strength <span class="value-display" id="spring-str-val">0.05</span></label>
                    <input type="range" id="springConstant" min="0.01" max="0.2" step="0.01" value="0.05">
                </div>
                
                <div class="control-group">
                    <label>Repulsion <span class="value-display" id="repulsion-val">-2000</span></label>
                    <input type="range" id="gravitationalConstant" min="-10000" max="-500" step="100" value="-2000">
                </div>
                
                <div class="control-group">
                    <label>Central Gravity <span class="value-display" id="gravity-val">0.01</span></label>
                    <input type="range" id="centralGravity" min="0" max="0.5" step="0.01" value="0.01">
                </div>
            </div>
            
            <div class="control-section">
                <h3>🎨 Display Options</h3>
                
                <div class="control-group">
                    <label>Node Size By</label>
                    <select id="nodeSizing">
                        <option value="count">Mention Count</option>
                        <option value="betweenness">Betweenness Centrality</option>
                        <option value="degree">Degree Centrality</option>
                        <option value="uniform">Uniform</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label>Min Node Size <span class="value-display" id="min-size-val">10</span></label>
                    <input type="range" id="minNodeSize" min="5" max="30" value="10">
                </div>
                
                <div class="control-group">
                    <label>Edge Width Factor <span class="value-display" id="edge-val">1</span></label>
                    <input type="range" id="edgeWidth" min="0.1" max="3" step="0.1" value="1">
                </div>
            </div>
            
            <div class="control-section">
                <h3>🔍 Filter</h3>
                
                <div class="control-group">
                    <label>Show Communities</label>
                    <select id="communityFilter" multiple size="5" style="height: auto;">
                        <option value="0" selected>Govt & Institutional (Red)</option>
                        <option value="1" selected>Electoral Process (Blue)</option>
                        <option value="2" selected>Fraud & Oversight (Green)</option>
                        <option value="3" selected>Opposition (Orange)</option>
                        <option value="4" selected>Media Critics (Purple)</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <label>Min Mentions <span class="value-display" id="min-mentions-val">0</span></label>
                    <input type="range" id="minMentions" min="0" max="50" value="0">
                </div>
            </div>
            
            <button onclick="updateNetwork()">🔄 Apply Changes</button>
            <button onclick="togglePhysics()" id="physics-toggle">⏸️ Pause Physics</button>
            <button onclick="resetView()" class="secondary">↺ Reset View</button>
            <button onclick="fitNetwork()" class="secondary">⊡ Fit to Screen</button>
            
            <div class="control-section">
                <h3>📊 Legend</h3>
                <div class="legend">
                    <div class="legend-item">
                        <div class="legend-color" style="background: #e74c3c;"></div>
                        <div>Government & Institutional</div>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #3498db;"></div>
                        <div>Electoral Process</div>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #2ecc71;"></div>
                        <div>Fraud & Oversight</div>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #f39c12;"></div>
                        <div>Opposition Candidates</div>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #9b59b6;"></div>
                        <div>Media Critics</div>
                    </div>
                </div>
                
                <div class="stats">
                    <div><strong>Visible:</strong> <span id="stats-nodes">38</span> nodes, <span id="stats-edges">227</span> edges</div>
                </div>
            </div>
        </div>
        
        <div id="mynetwork"></div>
    </div>
    
    <div id="info-panel">
        <h4 id="info-title"></h4>
        <div id="info-content"></div>
    </div>

    <script type="text/javascript">
        // Data
        const nodesDataFull = """ + json.dumps(nodes_data) + """;
        const edgesDataFull = """ + json.dumps(edges_data) + """;
        
        let network = null;
        let nodesDataset = null;
        let edgesDataset = null;
        
        function initNetwork() {
            const container = document.getElementById('mynetwork');
            
            nodesDataset = new vis.DataSet();
            edgesDataset = new vis.DataSet();
            
            const data = {
                nodes: nodesDataset,
                edges: edgesDataset
            };
            
            const options = {
                nodes: {
                    shape: 'dot',
                    font: {
                        size: 14,
                        face: 'Arial'
                    },
                    borderWidth: 2,
                    borderWidthSelected: 4
                },
                edges: {
                    smooth: {
                        type: 'continuous',
                        forceDirection: 'none'
                    },
                    color: {
                        color: '#cccccc',
                        highlight: '#667eea'
                    }
                },
                physics: {
                    enabled: true,
                    forceAtlas2Based: {
                        gravitationalConstant: -2000,
                        centralGravity: 0.01,
                        springLength: 150,
                        springConstant: 0.05,
                        damping: 0.4,
                        avoidOverlap: 0.5
                    },
                    solver: 'forceAtlas2Based',
                    stabilization: {
                        enabled: true,
                        iterations: 1500,
                        updateInterval: 50,
                        onlyDynamicEdges: false,
                        fit: true
                    },
                    adaptiveTimestep: true
                },
                interaction: {
                    hover: true,
                    tooltipDelay: 100,
                    navigationButtons: true,
                    keyboard: true
                }
            };
            
            network = new vis.Network(container, data, options);
            
            // Event handlers
            network.on("click", function(params) {
                if (params.nodes.length > 0) {
                    showNodeInfo(params.nodes[0]);
                } else {
                    hideNodeInfo();
                }
            });
            
            network.on("hoverNode", function(params) {
                document.body.style.cursor = 'pointer';
            });
            
            network.on("blurNode", function() {
                document.body.style.cursor = 'default';
            });
            
            // Auto-disable physics after stabilization - network starts paused
            network.once("stabilizationIterationsDone", function() {
                // Immediately disable physics after initial layout
                network.setOptions({ physics: false });
                console.log("Network stabilized - physics disabled (paused by default)");
                updatePhysicsButton(false);
            });
            
            network.on("stabilizationProgress", function(params) {
                const progress = Math.round((params.iterations / params.total) * 100);
                console.log("Stabilizing: " + progress + "%");
            });
            
            updateNetwork();
        }
        
        function updateNetwork() {
            const nodeSizing = document.getElementById('nodeSizing').value;
            const minNodeSize = parseInt(document.getElementById('minNodeSize').value);
            const edgeWidthFactor = parseFloat(document.getElementById('edgeWidth').value);
            const minMentions = parseInt(document.getElementById('minMentions').value);
            const selectedCommunities = Array.from(document.getElementById('communityFilter').selectedOptions).map(o => parseInt(o.value));
            
            // Filter nodes
            const filteredNodes = nodesDataFull.filter(node => 
                node.count >= minMentions && selectedCommunities.includes(node.community)
            );
            
            // Calculate node sizes
            const processedNodes = filteredNodes.map(node => {
                let size;
                if (nodeSizing === 'count') {
                    size = minNodeSize + (node.count * 1.5);
                } else if (nodeSizing === 'betweenness') {
                    size = minNodeSize + (node.betweenness * 200);
                } else if (nodeSizing === 'degree') {
                    size = minNodeSize + (node.degree * 50);
                } else {
                    size = 20;
                }
                
                return {
                    id: node.id,
                    label: node.label,
                    size: Math.max(size, minNodeSize),
                    color: node.color,
                    title: `${node.label}\nMentions: ${node.count}\nBetweenness: ${node.betweenness.toFixed(3)}\nCommunity: ${node.community}`,
                    ...node
                };
            });
            
            // Filter edges
            const nodeIds = new Set(processedNodes.map(n => n.id));
            const filteredEdges = edgesDataFull.filter(edge => 
                nodeIds.has(edge.from) && nodeIds.has(edge.to)
            ).map(edge => ({
                ...edge,
                width: edge.value * edgeWidthFactor
            }));
            
            // Update datasets
            nodesDataset.clear();
            edgesDataset.clear();
            nodesDataset.add(processedNodes);
            edgesDataset.add(filteredEdges);
            
            // Update stats
            document.getElementById('stats-nodes').textContent = processedNodes.length;
            document.getElementById('stats-edges').textContent = filteredEdges.length;
            
            // Update physics
            updatePhysics();
        }
        
        function updatePhysics() {
            const solver = document.getElementById('solver').value;
            const springLength = parseInt(document.getElementById('springLength').value);
            const springConstant = parseFloat(document.getElementById('springConstant').value);
            const gravitationalConstant = parseInt(document.getElementById('gravitationalConstant').value);
            const centralGravity = parseFloat(document.getElementById('centralGravity').value);
            
            let physicsOptions = {
                enabled: true,
                stabilization: {
                    iterations: 1000
                }
            };
            
            if (solver === 'barnesHut') {
                physicsOptions.barnesHut = {
                    gravitationalConstant: gravitationalConstant,
                    centralGravity: centralGravity,
                    springLength: springLength,
                    springConstant: springConstant,
                    damping: 0.09,
                    avoidOverlap: 0.5
                };
                physicsOptions.solver = 'barnesHut';
            } else if (solver === 'forceAtlas2Based') {
                physicsOptions.forceAtlas2Based = {
                    gravitationalConstant: gravitationalConstant,
                    centralGravity: centralGravity,
                    springLength: springLength,
                    springConstant: springConstant,
                    damping: 0.4,
                    avoidOverlap: 0.5
                };
                physicsOptions.solver = 'forceAtlas2Based';
            } else {
                physicsOptions.repulsion = {
                    centralGravity: centralGravity,
                    springLength: springLength,
                    springConstant: springConstant,
                    nodeDistance: 200,
                    damping: 0.09
                };
                physicsOptions.solver = 'repulsion';
            }
            
            network.setOptions({ physics: physicsOptions });
        }
        
        function resetView() {
            network.fit();
        }
        
        function fitNetwork() {
            network.fit({
                animation: {
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }
            });
        }
        
        function showNodeInfo(nodeId) {
            const node = nodesDataFull.find(n => n.id === nodeId);
            if (!node) return;
            
            const panel = document.getElementById('info-panel');
            document.getElementById('info-title').textContent = node.label;
            document.getElementById('info-content').innerHTML = `
                <div class="info-row"><span class="info-label">Mentions:</span> ${node.count}</div>
                <div class="info-row"><span class="info-label">Betweenness:</span> ${node.betweenness.toFixed(4)}</div>
                <div class="info-row"><span class="info-label">Degree Centrality:</span> ${node.degree.toFixed(4)}</div>
                <div class="info-row"><span class="info-label">Community:</span> ${node.community}</div>
            `;
            panel.style.display = 'block';
        }
        
        function hideNodeInfo() {
            document.getElementById('info-panel').style.display = 'none';
        }
        
        function togglePhysics() {
            const currentState = network.physics.physicsEnabled;
            network.setOptions({ physics: !currentState });
            updatePhysicsButton(!currentState);
        }
        
        function updatePhysicsButton(enabled) {
            const button = document.getElementById('physics-toggle');
            if (enabled) {
                button.textContent = '⏸️ Pause Physics';
                button.style.background = '#667eea';
            } else {
                button.textContent = '▶️ Resume Physics';
                button.style.background = '#2ecc71';
            }
        }
        
        // Range input value displays
        document.getElementById('springLength').oninput = function() {
            document.getElementById('spring-val').textContent = this.value;
        };
        document.getElementById('springConstant').oninput = function() {
            document.getElementById('spring-str-val').textContent = this.value;
        };
        document.getElementById('gravitationalConstant').oninput = function() {
            document.getElementById('repulsion-val').textContent = this.value;
        };
        document.getElementById('centralGravity').oninput = function() {
            document.getElementById('gravity-val').textContent = this.value;
        };
        document.getElementById('minNodeSize').oninput = function() {
            document.getElementById('min-size-val').textContent = this.value;
        };
        document.getElementById('edgeWidth').oninput = function() {
            document.getElementById('edge-val').textContent = this.value;
        };
        document.getElementById('minMentions').oninput = function() {
            document.getElementById('min-mentions-val').textContent = this.value;
        };
        
        // Initialize
        initNetwork();
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"Saved enhanced network to: {output_path}")

def main():
    print("=" * 60)
    print("Creating Enhanced Network Visualization")
    print("=" * 60)
    
    output_dir = "text_network/network_analysis_results"
    
    # Create enhanced visualization
    create_enhanced_network_html(
        f"{output_dir}/network_graph.pkl",
        f"{output_dir}/network_metadata.json",
        f"{output_dir}/full_network.html"
    )
    
    print("\n✓ Enhanced visualization complete!")
    print(f"\nOpen this file in your browser:")
    print(f"  {output_dir}/full_network.html")
    print("\nFeatures:")
    print("  • Adjustable physics settings (spring length, repulsion, gravity)")
    print("  • Multiple layout algorithms (Barnes-Hut, Force Atlas 2, Repulsion)")
    print("  • Filter by community and mention threshold")
    print("  • Adjustable node sizes and edge widths")
    print("  • Click nodes for detailed information")

if __name__ == "__main__":
    main()
