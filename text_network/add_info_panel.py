"""
Add collapsible information panel to network visualization
Reads README content and adds it as a slide-in drawer from the right
"""

import re

def read_readme():
    """Read and format README content for HTML"""
    with open('text_network/README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown to simple HTML
    # This is a simplified conversion - just handles the most common elements
    html_content = content
    
    # Convert headers
    html_content = re.sub(r'^# (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^#### (.+)$', r'<h5>\1</h5>', html_content, flags=re.MULTILINE)
    
    # Convert bold
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Convert lists
    html_content = re.sub(r'^\s*- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    
    # Convert horizontal rules
    html_content = re.sub(r'^---$', r'<hr>', html_content, flags=re.MULTILINE)
    
    # Wrap paragraphs
    lines = html_content.split('\n')
    processed = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('<li>'):
            if not in_list:
                processed.append('<ul>')
                in_list = True
            processed.append(line)
        else:
            if in_list:
                processed.append('</ul>')
                in_list = False
            processed.append(line)
    
    if in_list:
        processed.append('</ul>')
    
    return '\n'.join(processed)

def add_info_panel_to_html(input_html_path, output_html_path):
    """Add collapsible info panel to existing HTML"""
    
    # Read the existing HTML
    with open(input_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Read README content
    readme_html = read_readme()
    
    # CSS for the info panel
    info_panel_css = """
        #info-drawer {
            position: fixed;
            right: -600px;
            top: 0;
            width: 600px;
            height: 100vh;
            background: white;
            box-shadow: -4px 0 12px rgba(0,0,0,0.15);
            transition: right 0.3s ease-in-out;
            z-index: 1000;
            overflow-y: auto;
        }
        
        #info-drawer.open {
            right: 0;
        }
        
        #info-drawer-content {
            padding: 30px;
            font-size: 14px;
            line-height: 1.6;
        }
        
        #info-drawer-content h2 {
            font-size: 20px;
            color: #2c3e50;
            margin: 30px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }
        
        #info-drawer-content h2:first-child {
            margin-top: 0;
        }
        
        #info-drawer-content h3 {
            font-size: 16px;
            color: #34495e;
            margin: 20px 0 10px 0;
        }
        
        #info-drawer-content h4 {
            font-size: 14px;
            color: #4a5568;
            margin: 15px 0 8px 0;
        }
        
        #info-drawer-content h5 {
            font-size: 13px;
            color: #606971;
            margin: 12px 0 6px 0;
        }
        
        #info-drawer-content p {
            margin: 10px 0;
            color: #495057;
        }
        
        #info-drawer-content ul {
            margin: 10px 0;
            padding-left: 25px;
        }
        
        #info-drawer-content li {
            margin: 5px 0;
            color: #495057;
        }
        
        #info-drawer-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 13px;
        }
        
        #info-drawer-content table th {
            background: #f8f9fa;
            padding: 8px;
            text-align: left;
            border: 1px solid #dee2e6;
            font-weight: 600;
        }
        
        #info-drawer-content table td {
            padding: 8px;
            border: 1px solid #dee2e6;
        }
        
        #info-drawer-content hr {
            border: none;
            border-top: 1px solid #dee2e6;
            margin: 25px 0;
        }
        
        #info-drawer-content strong {
            font-weight: 600;
            color: #2c3e50;
        }
        
        #info-drawer-content code {
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 12px;
        }
        
        #info-toggle-btn {
            position: fixed;
            right: 20px;
            top: 80px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            transition: all 0.3s;
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        #info-toggle-btn:hover {
            background: #5568d3;
            transform: scale(1.1);
        }
        
        #info-toggle-btn.drawer-open {
            right: 620px;
        }
        
        #info-drawer-header {
            position: sticky;
            top: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 10;
        }
        
        #info-drawer-header h2 {
            margin: 0;
            font-size: 18px;
            border: none;
            padding: 0;
        }
        
        #info-drawer-close {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            transition: background 0.2s;
        }
        
        #info-drawer-close:hover {
            background: rgba(255,255,255,0.3);
        }
"""
    
    # Insert CSS before </style>
    html = html.replace('</style>', info_panel_css + '\n    </style>')
    
    # HTML for info drawer
    info_drawer_html = f"""
    <!-- Info Drawer -->
    <button id="info-toggle-btn" onclick="toggleInfoDrawer()">📊</button>
    
    <div id="info-drawer">
        <div id="info-drawer-header">
            <h2>📋 Analysis Report</h2>
            <button id="info-drawer-close" onclick="toggleInfoDrawer()">✕</button>
        </div>
        <div id="info-drawer-content">
            {readme_html}
        </div>
    </div>
"""
    
    # Insert drawer HTML before </body>
    html = html.replace('</body>', info_drawer_html + '\n</body>')
    
    # Add JavaScript for drawer toggle
    drawer_js = """
        function toggleInfoDrawer() {
            const drawer = document.getElementById('info-drawer');
            const btn = document.getElementById('info-toggle-btn');
            
            drawer.classList.toggle('open');
            btn.classList.toggle('drawer-open');
        }
"""
    
    # Insert JS before </script>
    html = html.replace('// Initialize\n        initNetwork();', 
                       'function toggleInfoDrawer() {\n            const drawer = document.getElementById(\'info-drawer\');\n            const btn = document.getElementById(\'info-toggle-btn\');\n            \n            drawer.classList.toggle(\'open\');\n            btn.classList.toggle(\'drawer-open\');\n        }\n        \n        // Initialize\n        initNetwork();')
    
    # Write output
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html)

def main():
    print("Adding information panel to network visualization...")
    
    input_path = 'text_network/network_analysis_results/full_network.html'
    output_path = 'text_network/network_analysis_results/full_network.html'
    
    add_info_panel_to_html(input_path, output_path)
    
    print(f"✓ Updated: {output_path}")
    print("\nThe visualization now includes a collapsible information panel")
    print("Click the 📊 button in the top-right to view the analysis report")

if __name__ == "__main__":
    main()
