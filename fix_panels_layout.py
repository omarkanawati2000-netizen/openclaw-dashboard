#!/usr/bin/env python3
"""
1. Make Revenue Tracker fill panel better
2. Make Sessions panel full-width with 3 columns
"""

HTML_FILE = "index.html"

# Add CSS for 3-column sessions layout and better revenue tracker
LAYOUT_CSS = '''
        /* Sessions 3-column layout for fullwidth panel */
        .panel-fullwidth .session-list-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
        }

        /* Make sessions more compact in grid */
        .panel-fullwidth .session-item {
            margin-bottom: 0;
        }

        /* Revenue tracker - remove excessive margins */
        .revenue-stream:last-child {
            margin-bottom: 0;
        }

        /* Mobile: stack sessions */
        @media (max-width: 768px) {
            .panel-fullwidth .session-list-grid {
                grid-template-columns: 1fr;
            }
        }'''

def main():
    print("Fixing panel layouts...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add layout CSS
    if '/* Sessions 3-column layout' not in html:
        html = html.replace('        /* Taller panel-content for fullwidth panels */',
                           LAYOUT_CSS + '\n\n        /* Taller panel-content for fullwidth panels */')
        print("[OK] Added layout CSS")
    
    # Make Sessions panel full-width
    if '<!-- Sessions Tracker -->' in html:
        html = html.replace(
            '<!-- Sessions Tracker -->\n            <div class="panel">',
            '<!-- Sessions Tracker -->\n            <div class="panel panel-fullwidth">'
        )
        print("[OK] Made Sessions panel full-width")
    
    # Update session rendering to use grid (need to modify JavaScript)
    # Find renderSessions function and wrap session items in grid
    old_render_sessions = "sessionList.innerHTML = data.sessions.map(session => `"
    new_render_sessions = "const sessionHTML = data.sessions.map(session => `"
    
    if old_render_sessions in html:
        html = html.replace(old_render_sessions, new_render_sessions)
        
        # Find where it closes the map and add grid wrapper
        old_close = "            `).join('');"
        new_close = "            `).join('');\n            sessionList.innerHTML = `<div class=\"session-list-grid\">${sessionHTML}</div>`;"
        
        # Find in renderSessions function
        render_sessions_start = html.find('function renderSessions()')
        render_sessions_end = html.find('function refreshDashboard()', render_sessions_start)
        
        if render_sessions_start > 0 and render_sessions_end > 0:
            section = html[render_sessions_start:render_sessions_end]
            if old_close in section:
                section = section.replace(old_close, new_close)
                html = html[:render_sessions_start] + section + html[render_sessions_end:]
                print("[OK] Updated renderSessions to use 3-column grid")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed panel layouts")
    print("\nChanges:")
    print("- Sessions panel now full-width (spans entire dashboard)")
    print("- Sessions displayed in 3 columns (better use of space)")
    print("- Revenue tracker margins optimized")
    print("- Mobile: sessions stack to 1 column")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Make Sessions full-width with 3 columns, optimize Revenue Tracker' && git push")

if __name__ == "__main__":
    main()
