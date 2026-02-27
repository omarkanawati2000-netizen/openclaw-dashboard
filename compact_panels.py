#!/usr/bin/env python3
"""Make panels compact with scrollable content"""

HTML_FILE = "index.html"

# Add scrollable panel styles
COMPACT_STYLES = '''
        /* Compact, scrollable panels */
        .panel-content {
            max-height: 300px;
            overflow-y: auto;
            overflow-x: hidden;
        }

        /* Custom scrollbar */
        .panel-content::-webkit-scrollbar {
            width: 8px;
        }

        .panel-content::-webkit-scrollbar-track {
            background: var(--bg-dark);
        }

        .panel-content::-webkit-scrollbar-thumb {
            background: var(--orange-dim);
            border-radius: 4px;
        }

        .panel-content::-webkit-scrollbar-thumb:hover {
            background: var(--orange);
        }

        /* Make panels more compact */
        .panel {
            max-height: 500px;
        }
'''

def main():
    print("Making panels compact and scrollable...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add compact styles before mobile responsive section
    if '/* Compact, scrollable panels */' not in html:
        html = html.replace('        /* Enhanced Mobile Responsive */',
                           COMPACT_STYLES + '\n        /* Enhanced Mobile Responsive */')
        print("[OK] Added compact panel styles")
    else:
        print("[SKIP] Styles already exist")
    
    # Update mobile collapsible max-height
    html = html.replace('max-height: 400px;', 'max-height: 300px;')
    print("[OK] Reduced mobile panel height to 300px")
    
    # Make sure all content areas are wrapped in panel-content divs
    # Already done, but let's verify the main scrollable sections
    
    # System Health panel - wrap content
    if '<div class="health-item">' in html and 'panel-content' not in html.split('<div class="health-item">')[0][-200:]:
        # Need to wrap health items
        html = html.replace(
            '<div class="health-item">',
            '<div class="panel-content"><div class="health-item">',
            1  # Only first occurrence
        )
        # Find where to close the wrapper (before error log section)
        html = html.replace(
            '<div style="margin-top: 1.5rem; margin-bottom: 0.5rem;">',
            '</div><div style="margin-top: 1.5rem; margin-bottom: 0.5rem;">',
            1
        )
        print("[OK] Wrapped System Health content")
    
    # Content Engine - already has sections, just make sure they're scrollable
    # Revenue Tracker - add wrapper
    if 'Revenue Tracker' in html:
        # Find revenue streams section
        revenue_section = html.find('<div class="revenue-stream">')
        if revenue_section > 0:
            before = html[:revenue_section]
            if 'panel-content' not in before[-500:]:
                # Need to wrap
                html = html.replace(
                    '<div class="revenue-stream">',
                    '<div class="panel-content"><div class="revenue-stream">',
                    1
                )
                # Close before stat-box (monthly target)
                html = html.replace(
                    '<div class="stat-box">\n                    <div class="stat-label">Monthly Target:',
                    '</div><div class="stat-box">\n                    <div class="stat-label">Monthly Target:',
                    1
                )
                print("[OK] Wrapped Revenue Tracker content")
    
    # API Usage - wrap items
    if 'API Usage Tracker' in html:
        api_section = html.find('<!-- API Usage Tracker -->')
        if api_section > 0:
            # Find first api-item after the header
            search_start = html.find('<div class="api-item">', api_section)
            if search_start > 0:
                before = html[:search_start]
                if 'panel-content' not in before[-500:]:
                    html = html.replace(
                        '<div class="api-item">',
                        '<div class="panel-content"><div class="api-item">',
                        1
                    )
                    # Close before Sessions Tracker panel
                    html = html.replace(
                        '<!-- Sessions Tracker -->',
                        '</div>\n\n            <!-- Sessions Tracker -->',
                        1
                    )
                    print("[OK] Wrapped API Usage content")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Made panels compact and scrollable")
    print("\nChanges:")
    print("- Max height: 300px per panel")
    print("- Scrollbars appear when content exceeds height")
    print("- Orange-themed scrollbars")
    print("- All panels now have scroll wheels")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Make panels compact with scrollbars' && git push")

if __name__ == "__main__":
    main()
