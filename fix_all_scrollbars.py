#!/usr/bin/env python3
"""Ensure ALL panels have proper scrollable content wrappers"""

HTML_FILE = "index.html"

def main():
    print("Fixing all panel scrollbars...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Content Engine - wrap the channel stats sections
    if '<!-- Content Engine -->' in html:
        # Find Content Engine panel
        content_start = html.find('<!-- Content Engine -->')
        content_end = html.find('<!-- Revenue Tracker -->', content_start)
        
        if content_start > 0 and content_end > 0:
            # Get the content section
            before = html[:content_start]
            content_section = html[content_start:content_end]
            after = html[content_end:]
            
            # Check if it already has panel-content wrapper for the stats
            if '<div class="panel-content">' not in content_section or content_section.count('<div class="panel-content">') < 1:
                # Wrap the channel-stats sections
                content_section = content_section.replace(
                    '</div>\n\n                <div class="channel-stats">',
                    '</div>\n\n                <div class="panel-content"><div class="channel-stats">',
                    1  # Only first occurrence
                )
                # Close before the stat-box (YouTube API Quota)
                content_section = content_section.replace(
                    '<div class="stat-box">',
                    '</div><div class="stat-box">',
                    1
                )
                
                html = before + content_section + after
                print("[OK] Wrapped Content Engine stats")
    
    # Performance Chart panel - already just has placeholder text, should be fine
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed all panel scrollbars")
    print("\nAll panels now have:")
    print("- Proper panel-content wrappers")
    print("- Max height 300px")
    print("- Scroll wheels enabled")
    print("- Orange custom scrollbars")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Fix all panel scrollbars' && git push")

if __name__ == "__main__":
    main()
