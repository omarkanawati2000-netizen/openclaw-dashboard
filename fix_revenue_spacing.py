#!/usr/bin/env python3
"""Add spacing above Monthly Target box in Revenue Tracker"""

HTML_FILE = "index.html"

# CSS to add spacing
SPACING_CSS = '''
        /* Revenue Tracker - separate monthly target */
        .revenue-stream:last-child + .stat-box {
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #333;
        }'''

def main():
    print("Adding spacing to Revenue Tracker...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add spacing CSS
    if '/* Revenue Tracker - separate monthly target */' not in html:
        html = html.replace('        /* Revenue tracker - remove excessive margins */',
                           SPACING_CSS + '\n\n        /* Revenue tracker - remove excessive margins */')
        print("[OK] Added monthly target spacing CSS")
    else:
        print("[SKIP] CSS already exists")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Added spacing above Monthly Target")
    print("\nChanges:")
    print("- 2rem top margin above Monthly Target")
    print("- 1.5rem top padding")
    print("- Subtle border-top separator")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Add spacing above Monthly Target in Revenue Tracker' && git push")

if __name__ == "__main__":
    main()
