#!/usr/bin/env python3
"""Move Monthly Target box down with more spacing"""

HTML_FILE = "index.html"

def main():
    print("Moving Monthly Target box lower...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find the Monthly Target stat-box in Revenue Tracker and add a specific class
    if 'Monthly Target: $10,000' in html:
        # Add a class to the Monthly Target box
        html = html.replace(
            '<div class="stat-box">\n                    <div class="stat-label">Monthly Target:',
            '<div class="stat-box monthly-target-box">\n                    <div class="stat-label">Monthly Target:'
        )
        print("[OK] Added monthly-target-box class")
    
    # Add aggressive CSS for the monthly target box
    monthly_target_css = '''
        /* Monthly Target - push down into empty space */
        .monthly-target-box {
            margin-top: 4rem !important;
            padding-top: 2rem;
            border-top: 2px solid #444;
        }'''
    
    if '/* Monthly Target - push down' not in html:
        # Find where to insert the CSS
        html = html.replace(
            '        /* Revenue Tracker - separate monthly target */',
            monthly_target_css + '\n\n        /* Revenue Tracker - separate monthly target */'
        )
        print("[OK] Added aggressive monthly target CSS")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Monthly Target box will be pushed down significantly")
    print("\nChanges:")
    print("- 4rem top margin (very large spacing)")
    print("- 2rem top padding")
    print("- Thicker border separator (2px)")
    print("- !important to override other styles")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Push Monthly Target box down significantly' && git push")

if __name__ == "__main__":
    main()
