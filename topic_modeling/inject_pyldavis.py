#!/usr/bin/env python3
"""
Add pyLDAvis interactive data to the comprehensive presentation HTML.
This reads the existing comprehensive HTML and injects the pyLDAvis JavaScript.
"""

import re
from pathlib import Path

def extract_ldavis_data(html_path):
    """Extract pyLDAvis data from HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the ldavis data object
    pattern = r'var ldavis_el\d+_data = ({.*?});'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Warning: Could not find ldavis data in {html_path}")
        return "{}" 
    
    return match.group(1)

def inject_pyldavis_data(html_file, comprehensive_html_backup):
    """Inject pyLDAvis data into the comprehensive HTML."""
    
    # Try to read politics data from the file (it may have just been generated)
    politics_data = extract_ldavis_data("topic_modeling/lda_visualization.html")
    
    # Read scam and others pyLDAvis data
    scam_data = extract_ldavis_data("topic_modeling/scam_category/lda_visualization.html")
    others_data = extract_ldavis_data("topic_modeling/others_category/lda_visualization.html")
    
    # Read the comprehensive HTML template
    with open(comprehensive_html_backup, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create the JavaScript to inject
    viz_script = f'''
    <script>
        // LDA Visualization Data
        var politics_data = {politics_data};
        var scam_data = {scam_data};
        var others_data = {others_data};
        
        // Initialize visualizations if data exists
        if (Object.keys(scam_data).length > 0) {{
            new LDAvis("#ldavis-scam", scam_data);
        }}
        
        if (Object.keys(others_data).length > 0) {{
            new LDAvis("#ldavis-others", others_data);
        }}
        
        // Politics note
        if (Object.keys(politics_data).length === 0) {{
            document.getElementById("ldavis-politics").innerHTML = 
                '<div class="alert alert-warning">' +
                '<strong>⚠️ Note:</strong> Politics interactive visualization needs to be regenerated. ' +
                'Run: <code>python3 run_lda_analysis.py topic_modeling/politics_hoax_text.csv topic_modeling "10"</code> ' +
                'to create the politics pyLDAvis visualization.' +
                '</div>';
        }} else {{
            new LDAvis("#ldavis-politics", politics_data);
        }}
    </script>
'''
    
    # Inject before closing body tag
    html_content = html_content.replace('</body>', viz_script + '\n</body>')
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Injected pyLDAvis data into {html_file}")
    print(f"  - Scam visualization: {'✓ Working' if len(scam_data) > 10 else '✗ Missing'}")
    print(f"  - Others visualization: {'✓ Working' if len(others_data) > 10 else '✗ Missing'}")
    print(f"  - Politics visualization: ⚠️  Needs regeneration")

def main():
    html_file = "topic_modeling/lda_visualization.html"
    inject_pyldavis_data(html_file)
    print(f"\n✅ Comprehensive presentation page ready: {html_file}")
    print(f"   Open in browser to view full analysis with interactive visualizations")

if __name__ == "__main__":
    main()
