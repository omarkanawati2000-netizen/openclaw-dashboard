#!/usr/bin/env python3
"""
Add Sessions Tracker panel to OpenClaw Dashboard
"""

import re

HTML_FILE = "index.html"

# Sessions panel HTML
SESSIONS_PANEL = '''
            <!-- Sessions Tracker -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">💬 Active Sessions</div>
                    <div class="panel-badge" id="sessionCount">0 Sessions</div>
                </div>
                <div id="sessionList"></div>
            </div>'''

# Sessions CSS
SESSIONS_CSS = '''
        /* Sessions Tracker */
        .session-item {
            background: var(--bg-dark);
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-radius: 4px;
            border-left: 3px solid var(--orange);
            transition: all 0.2s;
        }

        .session-item:hover {
            background: var(--bg-hover);
        }

        .session-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .session-name {
            font-weight: 600;
            font-size: 1.05rem;
        }

        .session-channel {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .channel-discord {
            background: #5865F2;
            color: white;
        }

        .channel-telegram {
            background: #0088cc;
            color: white;
        }

        .channel-unknown {
            background: var(--text-dim);
            color: var(--bg-dark);
        }

        .session-meta {
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }

        .session-tokens {
            font-size: 0.8rem;
            color: var(--orange);
        }
'''

# Sessions JavaScript
SESSIONS_JS = '''
        function renderSessions() {
            const data = dashboardData || mockData;
            const sessionList = document.getElementById('sessionList');
            
            if (!data.sessions || data.sessions.length === 0) {
                sessionList.innerHTML = '<div style="color: var(--text-dim); text-align: center; padding: 2rem;">No active sessions</div>';
                return;
            }
            
            sessionList.innerHTML = data.sessions.map(session => `
                <div class="session-item">
                    <div class="session-header">
                        <div class="session-name">${session.name}</div>
                        <div class="session-channel channel-${session.channel}">${session.channel}</div>
                    </div>
                    <div class="session-meta">
                        Model: ${session.model} • Kind: ${session.kind}
                    </div>
                    <div class="session-meta">
                        Last active: ${session.lastActive}
                    </div>
                    <div class="session-tokens">
                        ${session.tokens.toLocaleString()} tokens used
                    </div>
                </div>
            `).join('');
            
            document.getElementById('sessionCount').textContent = `${data.sessions.length} Active`;
        }
'''

def main():
    print("Adding Sessions Tracker to dashboard...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add sessions panel before closing dashboard-grid
    if '<!-- Sessions Tracker -->' not in html:
        html = html.replace('</div>\n    </div>\n\n    <script>', 
                           SESSIONS_PANEL + '\n        </div>\n    </div>\n\n    <script>')
        print("[OK] Added sessions panel HTML")
    else:
        print("[SKIP] Sessions panel already exists")
    
    # 2. Add sessions CSS before closing style tag
    if '.session-item {' not in html:
        html = html.replace('        @keyframes spin {', 
                           SESSIONS_CSS + '\n        @keyframes spin {')
        print("[OK] Added sessions CSS")
    else:
        print("[SKIP] Sessions CSS already exists")
    
    # 3. Add renderSessions function before refreshDashboard
    if 'function renderSessions()' not in html:
        html = html.replace('        function refreshDashboard() {',
                           SESSIONS_JS + '\n        function refreshDashboard() {')
        print("[OK] Added renderSessions() function")
    else:
        print("[SKIP] renderSessions() already exists")
    
    # 4. Add renderSessions() call to refreshDashboard
    if 'renderSessions();' not in html:
        # Find refreshDashboard function and add renderSessions() call
        html = re.sub(
            r'(function refreshDashboard\(\) \{[^\}]*renderStats\(\);)',
            r'\1\n            renderSessions();',
            html
        )
        print("[OK] Added renderSessions() to refreshDashboard()")
    else:
        print("[SKIP] renderSessions() call already exists")
    
    # 5. Add mock sessions data if not present
    if 'sessions:' not in html:
        # Add sessions array to mockData
        mock_sessions = '''            sessions: [
                { name: 'Discord #general', channel: 'discord', kind: 'group', model: 'claude-sonnet-4-5', tokens: 89000, lastActive: '2 min ago', sessionKey: 'agent:main:discord:channel:1468193294906425430' },
                { name: 'Telegram Retards v2', channel: 'telegram', kind: 'group', model: 'claude-sonnet-4-5', tokens: 45000, lastActive: '1 hour ago', sessionKey: 'agent:main:telegram:-1003146730450' },
            ],'''
        
        html = html.replace('            stats: {', mock_sessions + '\n            stats: {')
        print("[OK] Added mock sessions data")
    else:
        print("[SKIP] Sessions data already exists")
    
    # Write updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Updated {HTML_FILE}")
    print("\nNext steps:")
    print("1. Open index.html in browser to test")
    print("2. git add index.html data.json")
    print("3. git commit -m 'Add sessions tracker panel'")
    print("4. git push")

if __name__ == "__main__":
    main()
