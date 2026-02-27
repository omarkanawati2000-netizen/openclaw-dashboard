#!/usr/bin/env python3
"""Add sorting options to Bot Status panel"""

HTML_FILE = "index.html"

# CSS for bot sort dropdown (reuse session sort styles)
BOT_SORT_CSS = '''
        /* Bot sort dropdown */
        .bot-sort {
            display: inline-block;
            margin-left: 1rem;
        }

        .bot-sort select {
            background: var(--bg-dark);
            color: var(--text-primary);
            border: 1px solid var(--orange-dim);
            border-radius: 4px;
            padding: 0.25rem 0.5rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            cursor: pointer;
        }

        .bot-sort select:hover {
            border-color: var(--orange);
        }'''

def main():
    print("Adding bot sorting...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add bot sort CSS
    if '/* Bot sort dropdown */' not in html:
        html = html.replace('        /* Session sort dropdown */',
                           BOT_SORT_CSS + '\n\n        /* Session sort dropdown */')
        print("[OK] Added bot sort CSS")
    
    # Add sort dropdown to Bot Status panel header
    if '<!-- Bot Status -->' in html:
        # Find the panel header badge
        if '<div class="panel-badge" id="activeBots">' in html:
            html = html.replace(
                '<div class="panel-badge" id="activeBots">0 Running</div>',
                '''<div class="panel-badge" id="activeBots">0 Running</div>
                    <div class="bot-sort">
                        <select id="botSortBy" onchange="sortAndRenderBots()">
                            <option value="status">Sort: Status</option>
                            <option value="lastRun">Sort: Recent</option>
                            <option value="nextRun">Sort: Next Run</option>
                        </select>
                    </div>'''
            )
            print("[OK] Added sort dropdown to Bot Status header")
    
    # Add sorting JavaScript
    bot_sort_js = '''
        let currentBotSort = 'status';
        
        function sortAndRenderBots() {
            currentBotSort = document.getElementById('botSortBy').value;
            renderBots();
        }
        
        function sortBots(bots, sortBy) {
            const sorted = [...bots];
            
            if (sortBy === 'lastRun') {
                // Sort by last run (most recent first)
                // "X min ago" < "X hours ago" < "X days ago"
                sorted.sort((a, b) => {
                    return parseTimeAgo(a.lastRun) - parseTimeAgo(b.lastRun);
                });
            } else if (sortBy === 'nextRun') {
                // Sort by next run (soonest first)
                sorted.sort((a, b) => {
                    return parseTimeNext(a.nextRun) - parseTimeNext(b.nextRun);
                });
            } else {
                // Sort by status (running first, then idle, then error)
                const statusOrder = { 'running': 0, 'ok': 1, 'idle': 2, 'error': 3 };
                sorted.sort((a, b) => {
                    return (statusOrder[a.status] || 4) - (statusOrder[b.status] || 4);
                });
            }
            
            return sorted;
        }
        
        function parseTimeAgo(timeStr) {
            // Parse "X min ago", "X hours ago", "X days ago" into minutes
            if (!timeStr || timeStr === 'Unknown') return 999999;
            
            const match = timeStr.match(/(\d+)\s*(min|hour|day|week)/i);
            if (!match) return 999999;
            
            const value = parseInt(match[1]);
            const unit = match[2].toLowerCase();
            
            if (unit.startsWith('min')) return value;
            if (unit.startsWith('hour')) return value * 60;
            if (unit.startsWith('day')) return value * 1440;
            if (unit.startsWith('week')) return value * 10080;
            
            return 999999;
        }
        
        function parseTimeNext(timeStr) {
            // Parse "Xm", "Xh", "Xd" into minutes
            if (!timeStr || timeStr === 'Unknown') return 999999;
            
            const match = timeStr.match(/(\d+)(m|h|d)/);
            if (!match) return 999999;
            
            const value = parseInt(match[1]);
            const unit = match[2];
            
            if (unit === 'm') return value;
            if (unit === 'h') return value * 60;
            if (unit === 'd') return value * 1440;
            
            return 999999;
        }
'''
    
    if 'function sortAndRenderBots()' not in html:
        html = html.replace('        let currentSessionSort = \'lastActive\';',
                           bot_sort_js + '\n        let currentSessionSort = \'lastActive\';')
        print("[OK] Added bot sorting functions")
    
    # Update renderBots to use sorting
    old_render_bots = 'const data = dashboardData || mockData;\n            const botList = document.getElementById(\'botList\');'
    new_render_bots = '''const data = dashboardData || mockData;
            const botList = document.getElementById('botList');
            
            // Sort bots based on current sort option
            const sortedBots = sortBots(data.bots || [], currentBotSort);'''
    
    if old_render_bots in html:
        html = html.replace(old_render_bots, new_render_bots)
        
        # Update to use sortedBots instead of data.bots
        html = html.replace(
            'botList.innerHTML = data.bots.map(bot => `',
            'botList.innerHTML = sortedBots.map(bot => `'
        )
        html = html.replace(
            'const runningCount = data.bots.filter(b => b.status === \'running\').length;',
            'const runningCount = sortedBots.filter(b => b.status === \'running\').length;'
        )
        html = html.replace(
            'const totalBots = data.bots.length;',
            'const totalBots = sortedBots.length;'
        )
        print("[OK] Updated renderBots to use sorting")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Added bot sorting")
    print("\nFeatures:")
    print("- Sort dropdown in Bot Status panel header")
    print("- Sort by: Status (running first), Recent (last run), Next Run (soonest)")
    print("- Default: Status (shows running bots first)")
    print("- Changes apply instantly")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Add bot sorting (Status/Recent/Next Run)' && git push")

if __name__ == "__main__":
    main()
