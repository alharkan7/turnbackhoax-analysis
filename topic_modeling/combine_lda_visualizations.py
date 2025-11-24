#!/usr/bin/env python3
"""
Combine multiple pyLDAvis visualizations into a single HTML file with tabs.

This script reads the individual LDA visualization HTML files for politics, scam,
and others categories, and combines them into a single file with tab navigation.
"""

import re
from pathlib import Path

def extract_ldavis_data(html_path):
    """
    Extract the key pyLDAvis data from an HTML file.
    
    Returns:
        dict with 'data' and 'config' JavaScript objects
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the ldavis data (var ldavis_el... = new LDAvis(...))
    # Pattern to find the LDAvis initialization
    data_pattern = r'var ldavis_el\d+_data = ({.*?});'
    data_match = re.search(data_pattern, content, re.DOTALL)
    
    if not data_match:
        raise ValueError(f"Could not find ldavis data in {html_path}")
    
    ldavis_data = data_match.group(1)
    
    return ldavis_data

def create_combined_html(politics_html, scam_html, others_html, output_html):
    """
    Create a combined HTML file with tabs for all three visualizations.
    """
    print("Creating combined LDA visualization...")
    
    # Read the three visualization HTMLs
    print(f"  Reading politics visualization...")
    politics_data = extract_ldavis_data(politics_html)
    
    print(f"  Reading scam visualization...")
    scam_data = extract_ldavis_data(scam_html)
    
    print(f"  Reading others visualization...")
    others_data = extract_ldavis_data(others_html)
    
    # Create combined HTML with tabs
    combined_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>LDA Topic Modeling - All Categories</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v3.0.0.css">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 20px auto;
            padding: 0 20px;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 0;
            border-bottom: 2px solid #ddd;
            background-color: white;
            padding: 10px 20px 0 20px;
            border-radius: 8px 8px 0 0;
        }}
        
        .tab-button {{
            padding: 12px 30px;
            border: none;
            background-color: transparent;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            border-radius: 4px 4px 0 0;
        }}
        
        .tab-button:hover {{
            background-color: #f8f9fa;
            color: #333;
        }}
        
        .tab-button.active {{
            color: #667eea;
            border-bottom-color: #667eea;
            background-color: #f8f9fa;
        }}
        
        .tab-content {{
            display: none;
            background-color: white;
            padding: 30px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 1.8em;
            font-weight: 700;
            color: #333;
        }}
        
        #ldavis-container {{
            margin-top: 20px;
        }}
        
        .description {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #764ba2;
        }}
        
        .description h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        
        .description p {{
            margin: 0;
            color: #666;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 LDA Topic Modeling Analysis</h1>
        <p>Interactive Exploration of Hoax Narratives from TurnBackHoax.id</p>
    </div>
    
    <div class="container">
        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'politics')">
                🏛️ Politics (10 Topics)
            </button>
            <button class="tab-button" onclick="openTab(event, 'scam')">
                ⚠️ Scam (5 Topics)
            </button>
            <button class="tab-button" onclick="openTab(event, 'others')">
                📰 Others (7 Topics)
            </button>
        </div>
        
        <!-- Politics Tab -->
        <div id="politics" class="tab-content active">
            <div class="description">
                <h3>Politics Category</h3>
                <p>Analysis of <strong>1,358 political hoaxes</strong> related to the 2024 Indonesian election. Topics include candidate attacks, election fraud narratives, and institutional distrust.</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Documents</div>
                    <div class="stat-value">1,358</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Topics</div>
                    <div class="stat-value">10</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Coherence</div>
                    <div class="stat-value">0.458</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Main Theme</div>
                    <div class="stat-value" style="font-size: 1.2em;">Candidate Attacks</div>
                </div>
            </div>
            <div id="ldavis-politics"></div>
        </div>
        
        <!-- Scam Tab -->
        <div id="scam" class="tab-content">
            <div class="description">
                <h3>Scam Category</h3>
                <p>Analysis of <strong>939 scam-related hoaxes</strong> including fake job offers, lottery scams, and fraudulent banking messages.</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Documents</div>
                    <div class="stat-value">939</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Topics</div>
                    <div class="stat-value">5</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Coherence</div>
                    <div class="stat-value">0.452</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Main Theme</div>
                    <div class="stat-value" style="font-size: 1.2em;">Fake Job Offers</div>
                </div>
            </div>
            <div id="ldavis-scam"></div>
        </div>
        
        <!-- Others Tab -->
        <div id="others" class="tab-content">
            <div class="description">
                <h3>Others Category</h3>
                <p>Analysis of <strong>1,449 miscellaneous hoaxes</strong> covering health, disasters, religion, and other non-political/non-scam topics.</p>
            </div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Documents</div>
                    <div class="stat-value">1,449</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Topics</div>
                    <div class="stat-value">7</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Coherence</div>
                    <div class="stat-value">0.461</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Main Theme</div>
                    <div class="stat-value" style="font-size: 1.2em;">Health & Disasters</div>
                </div>
            </div>
            <div id="ldavis-others"></div>
        </div>
    </div>
    
    <script src="https://d3js.org/d3.v5.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.4.0/pyLDAvis/js/ldavis.v3.0.0.js"></script>
    
    <script>
        // Tab switching function
        function openTab(evt, tabName) {{
            // Hide all tab contents
            var tabContents = document.getElementsByClassName("tab-content");
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove("active");
            }}
            
            // Remove active class from all buttons
            var tabButtons = document.getElementsByClassName("tab-button");
            for (var i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].classList.remove("active");
            }}
            
            // Show the selected tab and mark button as active
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}
        
        // LDA Visualization Data
        var politics_data = {politics_data};
        var scam_data = {scam_data};
        var others_data = {others_data};
        
        // Initialize visualizations
        new LDAvis("#ldavis-politics", politics_data);
        new LDAvis("#ldavis-scam", scam_data);
        new LDAvis("#ldavis-others", others_data);
    </script>
</body>
</html>'''
    
    # Write combined HTML
    print(f"  Writing combined HTML to {output_html}...")
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(combined_html)
    
    print(f"✓ Combined visualization created: {output_html}")

def main():
    """Main entry point."""
    base_dir = Path("topic_modeling")
    
    politics_html = base_dir / "lda_visualization.html"
    scam_html = base_dir / "scam_category" / "lda_visualization.html"
    others_html = base_dir / "others_category" / "lda_visualization.html"
    output_html = base_dir / "lda_visualization.html"
    
    # Check if all files exist
    for html_file in [politics_html, scam_html, others_html]:
        if not html_file.exists():
            print(f"Error: {html_file} not found!")
            return
    
    # Create combined visualization
    create_combined_html(politics_html, scam_html, others_html, output_html)
    
    print("\n" + "=" * 60)
    print("✓ COMBINED VISUALIZATION COMPLETE")
    print("=" * 60)
    print(f"\nOpen in browser: {output_html.absolute()}")
    print("\nFeatures:")
    print("  - Tab navigation between Politics/Scam/Others")
    print("  - Category statistics at a glance")
    print("  - Interactive pyLDAvis for each category")
    print("=" * 60)

if __name__ == "__main__":
    main()
