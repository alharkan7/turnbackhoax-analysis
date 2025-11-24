"""
Enhanced multi-category visualization with synced tabbed info drawer
"""

import json
import re

def parse_readme_by_category():
    """Parse README and separate content by category"""
    with open('text_network/README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by category sections
    sections = {}
    
    # Overview section (before categories)
    overview_match = re.search(r'^# Text Network Analysis Summary\n\n## Overview\n(.*?)\n---', content, re.DOTALL)
    if overview_match:
        sections['overview'] = overview_match.group(0)
    
    # Politics section
    politics_match = re.search(r'# Category 1: Politics Network\n(.*?)(?=\n# Category 2:|$)', content, re.DOTALL)
    if politics_match:
        sections['politics'] = '# Politics Network Analysis\n\n' + politics_match.group(1)
    
    # Scam section
    scam_match = re.search(r'# Category 2: Scam Network\n(.*?)(?=\n# Category 3:|$)', content, re.DOTALL)
    if scam_match:
        sections['scam'] = '# Scam Network Analysis\n\n' + scam_match.group(1)
    
    # Others section
    others_match = re.search(r'# Category 3: Others Network\n(.*?)(?=\n## Cross-Category|$)', content, re.DOTALL)
    if others_match:
        sections['others'] = '# Others Network Analysis\n\n' + others_match.group(1)
    
    # Cross-category comparison
    cross_match = re.search(r'## Cross-Category Comparison\n(.*?)(?=\n---\n\n# Methodology|$)', content, re.DOTALL)
    if cross_match:
        sections['comparison'] = '# Cross-Category Comparison\n\n' + cross_match.group(0)
    
    # Methodology
    methodology_match = re.search(r'# Methodology\n\n## Methodology\n(.*?)$', content, re.DOTALL)
    if methodology_match:
        sections['methodology'] = '# Methodology\n\n' + methodology_match.group(1)
    
    return sections

def create_enhanced_html_with_synced_tabs():
    """Create HTML with synced tabs"""
    
    # Parse README by category
    readme_sections = parse_readme_by_category()
    
    # Read network data 
    import pickle
    
    categories_data = {}
    for category in ['politics', 'scam', 'others']:
        with open(f'text_network/network_analysis_results/{category}/network_graph.pkl', 'rb') as f:
            G = pickle.load(f)
        with open(f'text_network/network_analysis_results/{category}/network_metadata.json', 'r') as f:
            metadata = json.load(f)
        
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
        
        categories_data[category] = {
            'nodes': nodes_data,
            'edges': edges_data,
            'stats': metadata['stats']
        }
    
    # Convert sections to JSON
    readme_json = json.dumps(readme_sections)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Turnbackhoax Text Network Analysis</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://unpkg.com/vis-network/styles/vis-network.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        #header h1 {{
            font-size: 20px;
            font-weight: 600;
        }}
        
        #info-toggle-btn {{
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 8px 20px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 500;
            width: auto;
        }}
        
        #info-toggle-btn:hover {{
            background: rgba(255,255,255,0.3);
            color: white;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 12px;
            color: #495057;
        }}
        
        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            flex-shrink: 0;
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
            width: 100%;
        }}
        
        #controls {{
            width: 320px;
            background: #f8f9fa;
            border-right: 1px solid #dee2e6;
            overflow-y: auto;
            padding: 20px;
            flex-shrink: 0;
        }}
        
        .tab-content {{
            flex: 1;
            display: none;
            position: relative;
            height: 100%;
            width: 100%;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .network-canvas {{
            width: 100%;
            height: 100%;
            background: white;
            position: absolute;
            top: 0;
            left: 0;
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
        
        /* Info Drawer Styles */
        #info-drawer {{
            position: fixed;
            right: -700px;
            top: 0;
            width: 700px;
            height: 100vh;
            background: white;
            box-shadow: -4px 0 12px rgba(0,0,0,0.15);
            transition: right 0.3s ease-in-out;
            z-index: 1000;
            display: flex;
            flex-direction: column;
        }}
        
        #info-drawer.open {{
            right: 0;
        }}
        
        #info-drawer-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        #info-drawer-header h2 {{
            margin: 0;
            font-size: 18px;
        }}
        
        #info-drawer-close {{
            background: transparent;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
            transition: transform 0.2s;
            width: auto;
            margin: 0;
        }}
        
        #info-drawer-close:hover {{
            background: transparent;
            transform: scale(1.1);
        }}
        
        /* Drawer Tabs */
        .drawer-tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
            padding: 0 20px;
        }}
        
        .drawer-tab {{
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            font-weight: 500;
            color: #6c757d;
            font-size: 13px;
        }}
        
        .drawer-tab:hover {{
            background: white;
            color: #495057;
        }}
        
        .drawer-tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }}
        
        #info-drawer-content {{
            flex: 1;
            overflow-y: auto;
        }}
        
        .drawer-content {{
            padding: 30px;
            font-size: 14px;
            line-height: 1.6;
            color: #2c3e50;
            display: none;
        }}
        
        .drawer-content.active {{
            display: block;
        }}
        
        #info-drawer-content h1 {{
            font-size: 24px;
            margin: 20px 0 15px 0;
            color: #667eea;
        }}
        
        #info-drawer-content h2 {{
            font-size: 20px;
            margin: 25px 0 12px 0;
            color: #2c3e50;
            padding-bottom: 8px;
            border-bottom: 2px solid #667eea;
        }}
        
        #info-drawer-content h3 {{
            font-size: 16px;
            margin: 20px 0 10px 0;
            color: #34495e;
        }}
        
        #info-drawer-content h4 {{
            font-size: 14px;
            margin: 15px 0 8px 0;
            color: #4a5568;
        }}
        
        #info-drawer-content p {{
            margin: 10px 0;
            color: #495057;
        }}
        
        #info-drawer-content ul,
        #info-drawer-content ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        
        #info-drawer-content li {{
            margin: 5px 0;
        }}
        
        #info-drawer-content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 13px;
        }}
        
        #info-drawer-content thead {{
            background: #f8f9fa;
        }}
        
        #info-drawer-content th {{
            padding: 10px;
            text-align: left;
            border: 1px solid #dee2e6;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        #info-drawer-content td {{
            padding: 8px 10px;
            border: 1px solid #dee2e6;
        }}
        
        #info-drawer-content tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        #info-drawer-content hr {{
            border: none;
            border-top: 2px solid #dee2e6;
            margin: 25px 0;
        }}
        
        #info-drawer-content strong {{
            font-weight: 600;
            color: #2c3e50;
        }}
        
        #info-drawer-content code {{
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 12px;
            color: #e83e8c;
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>Turnbackhoax Text Network Analysis</h1>
        <button id="info-toggle-btn" onclick="toggleInfoDrawer()">Analysis Report</button>
    </div>
    
    <div class="tabs" id="main-tabs">
        <div class="tab active" data-category="politics" onclick="switchMainTab('politics')">
            <div class="tab-label">
                <span>Politics</span>
                <span class="tab-badge">{categories_data['politics']['stats']['unique_entities']} entities</span>
            </div>
        </div>
        <div class="tab" data-category="scam" onclick="switchMainTab('scam')">
            <div class="tab-label">
                <span>Scam</span>
                <span class="tab-badge">{categories_data['scam']['stats']['unique_entities']} entities</span>
            </div>
        </div>
        <div class="tab" data-category="others" onclick="switchMainTab('others')">
            <div class="tab-label">
                <span>Others</span>
                <span class="tab-badge">{categories_data['others']['stats']['unique_entities']} entities</span>
            </div>
        </div>
    </div>
    
    <div id="container">
        <div id="controls">
            <div class="control-section">
                <h3>Physics Settings</h3>
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
                <h3>Display Options</h3>
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
            <button onclick="updateNetwork()">Apply Changes</button>
            <button onclick="togglePhysics()" id="physics-toggle">Pause Physics</button>
            <button onclick="fitNetwork()" class="secondary">Fit to Screen</button>
            <div class="control-section">
                <h3>Statistics</h3>
                <div class="stats" id="current-stats"></div>
            </div>
            <div class="control-section">
                <h3>Legend</h3>
                <div id="legend-container"></div>
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
    
    <!-- Info Drawer -->
    <div id="info-drawer">
        <div id="info-drawer-header">
            <h2>Analysis Report</h2>
            <button id="info-drawer-close" onclick="toggleInfoDrawer()">✕</button>
        </div>
        
        <div class="drawer-tabs">
            <div class="drawer-tab active" data-category="politics" onclick="switchDrawerTab('politics')">Politics</div>
            <div class="drawer-tab" data-category="scam" onclick="switchDrawerTab('scam')">Scam</div>
            <div class="drawer-tab" data-category="others" onclick="switchDrawerTab('others')">Others</div>
            <div class="drawer-tab" data-category="comparison" onclick="switchDrawerTab('comparison')">Comparison</div>
        </div>
        
        <div id="info-drawer-content">
            <div id="drawer-politics" class="drawer-content active"></div>
            <div id="drawer-scam" class="drawer-content"></div>
            <div id="drawer-others" class="drawer-content"></div>
            <div id="drawer-comparison" class="drawer-content"></div>
        </div>
    </div>

    <script>
        const networkData = {json.dumps(categories_data, indent=4)};
        const readmeContent = {readme_json};
        
        let networks = {{}};
        let currentCategory = 'politics';
        let networksFitted = {{}}; // Track which networks have been fitted to screen
        
        const communityColors = {{
            0: '#e74c3c', 1: '#3498db', 2: '#2ecc71', 
            3: '#f39c12', 4: '#9b59b6', 5: '#1abc9c',
            6: '#e67e22', 7: '#34495e'
        }};

        const communityLabels = {{
            'politics': {{
                0: 'Government & Institutional',
                1: 'Electoral Process',
                2: 'Fraud & Oversight',
                3: 'Opposition Candidates',
                4: 'Media Critics'
            }},
            'scam': {{
                0: 'Banking & Finance',
                1: 'Recruitment & Impersonation',
                2: 'Social Media Fraud',
                3: 'Digital Wallets (Gopay)',
                4: 'Digital Wallets (OVO)',
                5: 'Social Aid'
            }},
            'others': {{
                0: 'International Conflict',
                1: 'Health & Pandemic',
                2: 'Natural Disasters',
                3: 'Health Misinformation'
            }}
        }};
        
        // Render markdown for each section
        document.addEventListener('DOMContentLoaded', function() {{
            if (typeof marked !== 'undefined') {{
                marked.setOptions({{
                    breaks: true,
                    gfm: true
                }});
                
                // Render each category section
                Object.keys(readmeContent).forEach(key => {{
                    const elementId = 'drawer-' + key;
                    const element = document.getElementById(elementId);
                    if (element && readmeContent[key]) {{
                        element.innerHTML = marked.parse(readmeContent[key]);
                    }}
                }});
            }}
        }});
        
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
                networksFitted[category] = false; // Initially not fitted
                
                networks[category].once("stabilizationIterationsDone", function() {{
                    networks[category].setOptions({{ physics: false }});
                    // Fit only the default visible network (politics)
                    if (category === 'politics') {{
                        setTimeout(() => {{
                            networks[category].fit({{ animation: false }});
                            networksFitted[category] = true;
                        }}, 100);
                    }}
                    if (category === currentCategory) {{
                        updatePhysicsButton(false);
                    }}
                }});
                
                // Fallback: ensure fit is called even if stabilization event is missed or delayed
                if (category === 'politics') {{
                    setTimeout(() => {{
                        if (!networksFitted[category]) {{
                            networks[category].fit({{ animation: false }});
                            networksFitted[category] = true;
                        }}
                    }}, 2000);
                }}
                
                networks[category].on("click", function(params) {{
                    if (params.nodes.length > 0) {{
                        showNodeInfo(params.nodes[0], category);
                    }}
                }});
            }});
            
            updateStats();
            createLegend();
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
        
        function switchMainTab(category) {{
            currentCategory = category;
            
            // Update main tabs
            document.querySelectorAll('#main-tabs .tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelector(`#main-tabs .tab[data-category="${{category}}"]`).classList.add('active');
            
            // Update tab content
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.getElementById(category + '-content').classList.add('active');
            
            // Fit network to screen if not done yet
            if (!networksFitted[category]) {{
                setTimeout(() => {{
                    networks[category].fit({{ animation: false }});
                    networksFitted[category] = true;
                }}, 150);
            }}
            
            // Sync drawer tabs
            syncDrawerTab(category);
            
            updateStats();
            createLegend();
            updatePhysicsButton(networks[category].physics.physicsEnabled);
        }}
        
        function switchDrawerTab(category) {{
            // Update drawer tabs
            document.querySelectorAll('.drawer-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelector(`.drawer-tab[data-category="${{category}}"]`).classList.add('active');
            
            // Update drawer content
            document.querySelectorAll('.drawer-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.getElementById('drawer-' + category).classList.add('active');
            
            // Sync main tabs if it's a network category
            if (['politics', 'scam', 'others'].includes(category)) {{
                syncMainTab(category);
            }}
        }}
        
        function syncDrawerTab(category) {{
            document.querySelectorAll('.drawer-tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            const drawerTab = document.querySelector(`.drawer-tab[data-category="${{category}}"]`);
            if (drawerTab) {{
                drawerTab.classList.add('active');
                
                document.querySelectorAll('.drawer-content').forEach(content => {{
                    content.classList.remove('active');
                }});
                document.getElementById('drawer-' + category).classList.add('active');
            }}
        }}
        
        function syncMainTab(category) {{
            currentCategory = category;
            
            document.querySelectorAll('#main-tabs .tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            document.querySelector(`#main-tabs .tab[data-category="${{category}}"]`).classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.getElementById(category + '-content').classList.add('active');
            
            updateStats();
            createLegend();
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
            button.textContent = enabled ? 'Pause Physics' : 'Resume Physics';
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
                <div><b>Mentions:</b> ${{node.count}}</div>
                <div><b>Betweenness:</b> ${{node.betweenness.toFixed(4)}}</div>
                <div><b>Degree:</b> ${{node.degree.toFixed(4)}}</div>
                <div><b>Community:</b> ${{node.community}}</div>
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

        function createLegend() {{
            const container = document.getElementById('legend-container');
            container.innerHTML = '';
            
            // Get active communities in current network
            const activeCommunities = new Set();
            networkData[currentCategory].nodes.forEach(node => activeCommunities.add(node.community));
            
            Array.from(activeCommunities).sort((a, b) => a - b).forEach(commId => {{
                const color = communityColors[commId] || '#95a5a6';
                const label = (communityLabels[currentCategory] && communityLabels[currentCategory][commId]) 
                            ? communityLabels[currentCategory][commId] 
                            : `Community ${{commId}}`;
                
                const item = document.createElement('div');
                item.className = 'legend-item';
                item.innerHTML = `
                    <div class="legend-color" style="background: ${{color}}"></div>
                    <span>${{label}}</span>
                `;
                container.appendChild(item);
            }});
        }}
        
        function toggleInfoDrawer() {{
            const drawer = document.getElementById('info-drawer');
            drawer.classList.toggle('open');
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
    
    return html

def main():
    print("Creating visualization with synced tabs...")
    
    # Parse README by category
    readme_sections = parse_readme_by_category()
    print(f"Parsed README sections: {list(readme_sections.keys())}")
    
    html = create_enhanced_html_with_synced_tabs()
    
    output_path = 'text_network/network_analysis_results/multi_category_network.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Created: {output_path}")
    print("\nFeatures:")
    print("  • Tabbed interface for all three categories")
    print("  • Drawer with tabs for each category + comparison")
    print("  • SYNCED tabs - changing one updates the other!")
    print("  • Proper markdown rendering with marked.js")

if __name__ == "__main__":
    main()
