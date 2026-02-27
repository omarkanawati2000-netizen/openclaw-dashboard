#!/usr/bin/env python3
"""Fix duplicate dashboardData declaration"""

HTML_FILE = "index.html"

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the loadRealData function that has duplicate declaration
html = html.replace('''        // Data source (tries real data.json first, falls back to mock)
        let dashboardData = null;
        
        async function loadRealData() {
            try {
                const response = await fetch("data.json");
                if (response.ok) {
                    dashboardData = await response.json();
                    console.log("[OK] Loaded real data from data.json");
                    return true;
                }
            } catch (e) {
                console.warn("[WARN] Could not load data.json, using mock data");
            }
            return false;
        }
        
        ''', '')

# Make sure renderApiUsage and renderSessions are called
if 'renderApiUsage();' not in html:
    html = html.replace('renderStats();',
                       '''renderStats();
            renderApiUsage();
            renderSessions();''')

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("[OK] Fixed duplicate declaration")
print("- Removed loadRealData() function")
print("- Added renderApiUsage() and renderSessions() to refreshDashboard()")
