#!/usr/bin/env python3
"""Make Bot Status panel span full width"""

HTML_FILE = "index.html"

# Add CSS to make bot panel full-width
FULLWIDTH_CSS = '''
        /* Full-width panels */
        .panel-fullwidth {
            grid-column: 1 / -1;
        }'''

def main():
    print("Making Bot Status panel full-width...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add fullwidth CSS
    if '/* Full-width panels */' not in html:
        # Insert after panel styles
        html = html.replace('        /* Bot Status */',
                           FULLWIDTH_CSS + '\n\n        /* Bot Status */')
        print("[OK] Added full-width panel CSS")
    
    # Add fullwidth class to Bot Status panel
    if '<!-- Bot Status -->' in html:
        html = html.replace(
            '<!-- Bot Status -->\n            <div class="panel">',
            '<!-- Bot Status -->\n            <div class="panel panel-fullwidth">'
        )
        print("[OK] Made Bot Status panel full-width")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Bot Status panel now spans entire width")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Make Bot Status panel full-width' && git push")

if __name__ == "__main__":
    main()
