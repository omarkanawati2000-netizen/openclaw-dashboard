#!/usr/bin/env python3
"""
Fix mobile UI for OpenClaw Dashboard
- Better responsive design
- Collapsible panels
- Simplified mobile view
- Fix chart visibility
"""

import re

HTML_FILE = "index.html"

# Enhanced mobile CSS
MOBILE_CSS = '''
        /* Enhanced Mobile Responsive */
        @media (max-width: 768px) {
            body {
                font-size: 14px;
            }

            header {
                padding: 1rem;
            }

            h1 {
                font-size: 1.3rem;
            }

            .container {
                padding: 0.5rem;
            }

            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }

            .panel {
                padding: 1rem;
            }

            .panel-title {
                font-size: 1rem;
            }

            .panel-badge {
                font-size: 0.65rem;
                padding: 0.2rem 0.5rem;
            }

            /* Collapsible panels on mobile */
            .panel-content {
                max-height: 400px;
                overflow-y: auto;
            }

            .panel-content.collapsed {
                max-height: 0;
                overflow: hidden;
            }

            .panel-header {
                cursor: pointer;
                user-select: none;
            }

            .panel-header::after {
                content: '▼';
                margin-left: 0.5rem;
                font-size: 0.8rem;
                color: var(--text-dim);
            }

            .panel-header.collapsed::after {
                content: '▶';
            }

            /* Position items stack on mobile */
            .position-item {
                grid-template-columns: 1fr;
                gap: 0.5rem;
                padding: 0.75rem;
            }

            .position-item > div {
                display: flex;
                justify-content: space-between;
            }

            /* Bot items more compact */
            .bot-item {
                padding: 0.75rem;
                font-size: 0.85rem;
            }

            .bot-meta {
                font-size: 0.7rem;
            }

            /* Session items more compact */
            .session-item {
                padding: 0.75rem;
            }

            .session-meta {
                font-size: 0.75rem;
            }

            /* Stats grid better on mobile */
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.75rem;
            }

            .stat-number {
                font-size: 1.2rem;
            }

            /* Quick actions stack */
            .quick-actions {
                flex-direction: column;
                gap: 0.5rem;
            }

            .btn {
                width: 100%;
                padding: 0.6rem 1rem;
                font-size: 0.85rem;
            }

            /* Chart container better spacing */
            .chart-container {
                height: 150px;
                font-size: 0.8rem;
            }

            /* API items more compact */
            .api-item {
                padding: 0.75rem;
                margin-bottom: 0.75rem;
            }

            .api-header {
                font-size: 0.85rem;
            }

            /* Hide less critical elements on mobile */
            .hide-mobile {
                display: none !important;
            }

            /* Stat boxes more compact */
            .stat-box {
                padding: 0.75rem;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                font-size: 0.7rem;
            }

            .stat-value {
                font-size: 1.2rem;
            }

            /* Revenue/health items */
            .revenue-stream, .health-item {
                padding: 0.75rem 0;
            }
        }

        /* Extra small screens */
        @media (max-width: 480px) {
            h1 {
                font-size: 1.1rem;
            }

            .subtitle {
                font-size: 0.8rem;
            }

            .panel {
                padding: 0.75rem;
            }

            .bot-item, .session-item {
                padding: 0.5rem;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
'''

# Mobile-specific collapsible JS
MOBILE_JS = '''
        // Mobile: collapsible panels
        let collapsedPanels = new Set();
        
        function initMobileCollapse() {
            if (window.innerWidth <= 768) {
                document.querySelectorAll('.panel-header').forEach(header => {
                    header.onclick = function() {
                        const panel = this.closest('.panel');
                        const content = panel.querySelector('.panel-content') || 
                                       panel.querySelector('#botList')?.parentElement ||
                                       panel.querySelector('#positionList')?.parentElement ||
                                       panel.querySelector('#sessionList')?.parentElement;
                        
                        if (content) {
                            this.classList.toggle('collapsed');
                            content.classList.toggle('collapsed');
                        }
                    };
                });
            }
        }

        // Re-init on window resize
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(initMobileCollapse, 250);
        });
'''

def main():
    print("Fixing mobile UI...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Replace existing mobile CSS with enhanced version
    if '@media (max-width: 768px)' in html:
        # Find and replace the mobile media query section
        pattern = r'@media \(max-width: 768px\) \{[^}]*(?:\{[^}]*\}[^}]*)*\}'
        html = re.sub(pattern, '', html, flags=re.DOTALL)
        print("[OK] Removed old mobile CSS")
    
    # Add new mobile CSS before closing </style>
    html = html.replace('    </style>', MOBILE_CSS + '\n    </style>')
    print("[OK] Added enhanced mobile CSS")
    
    # 2. Wrap panel contents in .panel-content divs for collapsing
    # For bot panel
    html = html.replace('<div id="botList"></div>',
                       '<div class="panel-content"><div id="botList"></div></div>')
    
    # For trading panel
    html = html.replace('<div id="positionList"></div>',
                       '<div class="panel-content"><div id="positionList"></div></div>')
    
    # For sessions panel
    html = html.replace('<div id="sessionList"></div>',
                       '<div class="panel-content"><div id="sessionList"></div></div>')
    
    print("[OK] Added collapsible wrappers")
    
    # 3. Add mobile collapse JS before closing </script>
    if 'initMobileCollapse' not in html:
        html = html.replace('// Initial render', 
                           MOBILE_JS + '\n        // Initial render')
        print("[OK] Added mobile collapse JavaScript")
    
    # 4. Call initMobileCollapse after initial render
    if 'initMobileCollapse();' not in html:
        html = html.replace('refreshDashboard();\n        })();',
                           'refreshDashboard();\n            initMobileCollapse();\n        })();')
        print("[OK] Added initMobileCollapse() call")
    
    # 5. Add viewport meta tag if missing
    if 'viewport' not in html:
        html = html.replace('<meta charset="UTF-8">',
                           '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">')
        print("[OK] Enhanced viewport meta tag")
    
    # Write updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed {HTML_FILE} for mobile")
    print("\nMobile improvements:")
    print("- Collapsible panels (tap header to expand/collapse)")
    print("- Compact layout with better spacing")
    print("- Larger touch targets")
    print("- Simplified grid (1 column on mobile)")
    print("- Better font sizes")
    print("- Fixed chart visibility")
    print("- Scrollable panel content (max 400px)")
    print("\nTest on mobile and deploy:")
    print("git add index.html && git commit -m 'Improve mobile UI' && git push")

if __name__ == "__main__":
    main()
