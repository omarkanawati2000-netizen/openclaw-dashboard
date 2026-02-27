#!/usr/bin/env python3
"""Debug and fix data.json loading"""

HTML_FILE = "index.html"

# Enhanced loadData function with console logging
FIXED_LOAD_DATA = '''        // Fetch real data from data.json
        let dashboardData = null;
        
        async function loadData() {
            console.log('[DEBUG] Attempting to load data.json...');
            try {
                const response = await fetch('data.json');
                console.log('[DEBUG] Fetch response:', response.status, response.statusText);
                
                if (response.ok) {
                    dashboardData = await response.json();
                    console.log('[OK] Loaded real data:', {
                        positions: dashboardData.positions?.length || 0,
                        sessions: dashboardData.sessions?.length || 0,
                        bots: dashboardData.bots?.length || 0,
                        anthropicTokens: dashboardData.stats?.anthropicTokens || 0,
                        ytQuota: dashboardData.stats?.ytQuotaUsed || 0
                    });
                    return true;
                } else {
                    console.warn('[WARN] data.json fetch failed:', response.status);
                    return false;
                }
            } catch (e) {
                console.error('[ERROR] Failed to load data.json:', e.message);
                return false;
            }
        }
'''

def main():
    print("Fixing data loading with debugging...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find and replace the loadData function
    import re
    
    # Pattern to match the entire loadData section
    pattern = r'// Fetch real data from data\.json[\s\S]*?async function loadData\(\) \{[\s\S]*?\n        \}'
    
    if re.search(pattern, html):
        html = re.sub(pattern, FIXED_LOAD_DATA.strip(), html)
        print("[OK] Replaced loadData() function")
    else:
        print("[ERROR] Could not find loadData() function")
        # Try to find where to insert it
        if 'async function loadData()' in html:
            print("[INFO] loadData exists but pattern didn't match")
        else:
            print("[ERROR] loadData() doesn't exist at all!")
        return
    
    # Make sure data.json is in the same directory
    import os
    data_path = os.path.join(os.path.dirname(__file__), 'data.json')
    if os.path.exists(data_path):
        print(f"[OK] data.json exists at {data_path}")
        # Check file size
        size = os.path.getsize(data_path)
        print(f"[OK] data.json size: {size:,} bytes")
    else:
        print("[ERROR] data.json NOT FOUND!")
        return
    
    # Write updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Updated {HTML_FILE} with debug logging")
    print("\nDebugging added:")
    print("- Console logs for fetch status")
    print("- Logs show: positions, sessions, bots, tokens, quota")
    print("- Error logging if fetch fails")
    print("\nNext steps:")
    print("1. Open browser DevTools (F12)")
    print("2. Go to Console tab")
    print("3. Refresh dashboard")
    print("4. Look for [DEBUG] and [OK] messages")
    print("\nIf you see 'Failed to load data.json', data.json might not be deployed.")
    print("\nDeploy:")
    print("git add index.html data.json && git commit -m 'Fix data loading with debugging' && git push")

if __name__ == "__main__":
    main()
