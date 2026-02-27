#!/usr/bin/env python3
"""Fix API usage display to show real data from data.json"""

HTML_FILE = "index.html"

# Fixed renderApiUsage function
FIXED_RENDER_API = '''        function renderApiUsage() {
            const data = dashboardData || mockData;
            const stats = data.stats || {};
            
            // YouTube API
            const ytUsed = stats.ytQuotaUsed || 0;
            const ytPercent = (ytUsed / 10000) * 100;
            document.getElementById('ytApiUsage').textContent = `${ytUsed.toLocaleString()} / 10,000`;
            document.getElementById('ytApiBar').style.width = `${ytPercent}%`;
            const ytRemaining = 10000 - ytUsed;
            document.getElementById('ytApiMeta').textContent = `${ytRemaining.toLocaleString()} units remaining`;
            
            // OpenAI API
            const openaiUsed = stats.openaiUsage || 0;
            document.getElementById('openaiApiUsage').textContent = `${openaiUsed}%`;
            document.getElementById('openaiApiBar').style.width = `${openaiUsed}%`;
            document.getElementById('openaiApiMeta').textContent = openaiUsed > 0 ? `${100 - openaiUsed}% remaining` : 'Unknown usage';
            
            // Hyperliquid
            const hlStatus = stats.hyperliquidRate || 'Unknown';
            document.getElementById('hlApiUsage').textContent = hlStatus;
            const hlPercent = hlStatus === 'Good' ? 25 : hlStatus === 'Warning' ? 75 : hlStatus === 'Throttled' ? 100 : 0;
            document.getElementById('hlApiBar').style.width = `${hlPercent}%`;
            document.getElementById('hlApiMeta').textContent = hlStatus === 'Good' ? 'No rate limit issues' : 'Rate limit status';
            
            // Twitch API
            const twitchStatus = stats.twitchUsage || 'Unknown';
            document.getElementById('twitchApiUsage').textContent = twitchStatus;
            document.getElementById('twitchApiBar').style.width = '0%';
            document.getElementById('twitchApiMeta').textContent = 'Tracking not enabled';
            
            // Anthropic (total tokens from sessions)
            const anthropicTokens = stats.anthropicTokens || 0;
            const anthropicPercent = stats.anthropicPercent || 0;
            
            if (anthropicTokens > 0) {
                // Format large numbers: 4,300,535 → "4.3M"
                let tokenDisplay;
                if (anthropicTokens >= 1000000) {
                    tokenDisplay = (anthropicTokens / 1000000).toFixed(1) + 'M';
                } else if (anthropicTokens >= 1000) {
                    tokenDisplay = (anthropicTokens / 1000).toFixed(1) + 'K';
                } else {
                    tokenDisplay = anthropicTokens.toLocaleString();
                }
                
                document.getElementById('anthropicApiUsage').textContent = `${tokenDisplay} tokens`;
                document.getElementById('anthropicApiBar').style.width = `${Math.min(anthropicPercent, 100)}%`;
                
                const sessions = data.sessions || [];
                document.getElementById('anthropicApiMeta').textContent = `Across ${sessions.length} sessions`;
            } else {
                document.getElementById('anthropicApiUsage').textContent = '0 tokens';
                document.getElementById('anthropicApiBar').style.width = '0%';
                document.getElementById('anthropicApiMeta').textContent = 'No sessions active';
            }
        }
'''

def main():
    print("Fixing API usage display...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find and replace the renderApiUsage function
    import re
    
    # Pattern to match the entire function
    pattern = r'function renderApiUsage\(\) \{[\s\S]*?\n        \}'
    
    if re.search(pattern, html):
        html = re.sub(pattern, FIXED_RENDER_API.strip(), html)
        print("[OK] Replaced renderApiUsage() function")
    else:
        print("[ERROR] Could not find renderApiUsage() function")
        return
    
    # Write updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed {HTML_FILE}")
    print("\nAPI Usage will now show:")
    print("- OpenAI: 15% (from stats.openaiUsage)")
    print("- YouTube: 0 / 10,000 (from stats.ytQuotaUsed)")
    print("- Hyperliquid: Good (from stats.hyperliquidRate)")
    print("- Twitch: Unknown (from stats.twitchUsage)")
    print("- Anthropic: 4.3M tokens (from stats.anthropicTokens)")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Fix API usage display with real data' && git push")

if __name__ == "__main__":
    main()
