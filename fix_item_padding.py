#!/usr/bin/env python3
"""Add better padding to items inside scrollable panels"""

HTML_FILE = "index.html"

# Add padding to items that appear in scrollable panels
ITEM_PADDING_FIX = '''
        /* Better spacing for items in scrollable panels */
        .panel-content .bot-item,
        .panel-content .position-item,
        .panel-content .session-item,
        .panel-content .api-item,
        .panel-content .health-item,
        .panel-content .revenue-stream {
            margin-right: 0.5rem;
        }

        .panel-content .stat-box {
            margin-right: 0.5rem;
        }'''

def main():
    print("Adding better item padding...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add the item padding styles after panel-content styles
    if '/* Better spacing for items in scrollable panels */' not in html:
        # Find where to insert (after panel-content scrollbar styles)
        insertion_point = html.find('.panel-content::-webkit-scrollbar-thumb:hover {')
        if insertion_point > 0:
            # Find the closing brace
            next_brace = html.find('}', insertion_point)
            if next_brace > 0:
                # Insert after this style block
                html = html[:next_brace+1] + '\n' + ITEM_PADDING_FIX + html[next_brace+1:]
                print("[OK] Added item padding styles")
        else:
            print("[ERROR] Could not find insertion point")
            return
    else:
        print("[SKIP] Item padding already exists")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed item padding")
    print("\nChanges:")
    print("- All items inside panels now have 0.5rem right margin")
    print("- Content won't touch the scrollbar")
    print("- Cleaner, less clunky appearance")

if __name__ == "__main__":
    main()
