#!/usr/bin/env python3
"""Add sorting options to Sessions panel"""

HTML_FILE = "index.html"

# CSS for sort dropdown
SORT_CSS = '''
        /* Session sort dropdown */
        .session-sort {
            display: inline-block;
            margin-left: 1rem;
        }

        .session-sort select {
            background: var(--bg-dark);
            color: var(--text-primary);
            border: 1px solid var(--orange-dim);
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            cursor: pointer;
        }

        .session-sort select:hover {
            border-color: var(--orange);
        }'''

def main():
    print("Adding session sorting...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add sort CSS
    if '/* Session sort dropdown */' not in html:
        html = html.replace('        /* Mobile: stack sessions */',
                           SORT_CSS + '\n\n        /* Mobile: stack sessions */')
        print("[OK] Added sort CSS")
    
    # Add sort dropdown to Sessions panel header
    if '<!-- Sessions Tracker -->' in html:
        # Find the panel header
        sessions_start = html.find('<!-- Sessions Tracker -->')
        sessions_section = html[sessions_start:sessions_start+500]
        
        if '<div class="panel-badge" id="sessionCount">' in sessions_section:
            html = html.replace(
                '<div class="panel-badge" id="sessionCount">0 Sessions</div>',
                '''<div class="panel-badge" id="sessionCount">0 Sessions</div>
                    <div class="session-sort">
                        <select id="sessionSortBy" onchange="sortAndRenderSessions()">
                            <option value="lastActive">Sort: Recent</option>
                            <option value="tokens">Sort: Tokens</option>
                        </select>
                    </div>'''
            )
            print("[OK] Added sort dropdown to header")
    
    # Add sorting JavaScript
    sort_js = '''
        let currentSessionSort = 'lastActive';
        
        function sortAndRenderSessions() {
            currentSessionSort = document.getElementById('sessionSortBy').value;
            renderSessions();
        }
        
        function sortSessions(sessions, sortBy) {
            const sorted = [...sessions];
            
            if (sortBy === 'tokens') {
                // Sort by tokens (descending)
                sorted.sort((a, b) => (b.tokens || 0) - (a.tokens || 0));
            } else {
                // Sort by last active (already sorted from API, but ensure it)
                // Keep original order (assumes newest first from API)
            }
            
            return sorted;
        }
'''
    
    if 'function sortAndRenderSessions()' not in html:
        html = html.replace('        function renderSessions() {',
                           sort_js + '\n        function renderSessions() {')
        print("[OK] Added sorting functions")
    
    # Update renderSessions to use sorting
    old_render_sessions = 'const data = dashboardData || mockData;\n            const sessionList = document.getElementById(\'sessionList\');'
    new_render_sessions = '''const data = dashboardData || mockData;
            const sessionList = document.getElementById('sessionList');
            
            // Sort sessions based on current sort option
            const sortedSessions = sortSessions(data.sessions || [], currentSessionSort);'''
    
    if old_render_sessions in html:
        html = html.replace(old_render_sessions, new_render_sessions)
        
        # Update to use sortedSessions instead of data.sessions
        html = html.replace(
            'if (!data.sessions || data.sessions.length === 0) {',
            'if (!sortedSessions || sortedSessions.length === 0) {'
        )
        html = html.replace(
            'const sessionHTML = data.sessions.map(session => `',
            'const sessionHTML = sortedSessions.map(session => `'
        )
        html = html.replace(
            'document.getElementById(\'sessionCount\').textContent = `${data.sessions.length} Active`;',
            'document.getElementById(\'sessionCount\').textContent = `${sortedSessions.length} Active`;'
        )
        print("[OK] Updated renderSessions to use sorting")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Added session sorting")
    print("\nFeatures:")
    print("- Sort dropdown in Sessions panel header")
    print("- Sort by: Recent (last active) or Tokens (usage)")
    print("- Default: Recent (newest first)")
    print("- Changes apply instantly")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Add session sorting (Recent/Tokens)' && git push")

if __name__ == "__main__":
    main()
