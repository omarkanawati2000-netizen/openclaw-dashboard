#!/usr/bin/env python3
"""Fix panel content overflow issue"""

HTML_FILE = "index.html"

# Fixed panel content styles
FIXED_PANEL_CONTENT = '''        /* Compact, scrollable panels */
        .panel-content {
            max-height: 300px;
            overflow-y: auto;
            overflow-x: hidden;
            padding-right: 0.5rem;
            margin-right: -0.5rem;
        }

        /* Custom scrollbar */
        .panel-content::-webkit-scrollbar {
            width: 6px;
        }

        .panel-content::-webkit-scrollbar-track {
            background: transparent;
        }

        .panel-content::-webkit-scrollbar-thumb {
            background: var(--orange-dim);
            border-radius: 3px;
        }

        .panel-content::-webkit-scrollbar-thumb:hover {
            background: var(--orange);
        }

        /* Make panels more compact - remove max-height on panel itself */
        .panel {
            overflow: visible;
        }

        /* Ensure panel children don't overflow */
        .panel > * {
            overflow: visible;
        }'''

def main():
    print("Fixing panel overflow...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find and replace the panel-content styles
    import re
    
    # Remove old compact panel styles
    pattern = r'/\* Compact, scrollable panels \*/[\s\S]*?/\* Make panels more compact \*/[\s\S]*?\n        \}'
    
    if re.search(pattern, html):
        html = re.sub(pattern, FIXED_PANEL_CONTENT.strip(), html)
        print("[OK] Replaced panel-content styles")
    else:
        print("[ERROR] Could not find panel styles to replace")
        return
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed panel overflow")
    print("\nChanges:")
    print("- Added padding-right to panel-content")
    print("- Removed max-height from .panel (was causing double border)")
    print("- Made scrollbar thinner (6px)")
    print("- Transparent scrollbar track")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Fix panel overflow and borders' && git push")

if __name__ == "__main__":
    main()
