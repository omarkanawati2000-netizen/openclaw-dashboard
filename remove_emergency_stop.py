#!/usr/bin/env python3
"""Remove Emergency Stop button - security risk on public site"""

HTML_FILE = "index.html"

def main():
    print("Removing Emergency Stop button...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove the Emergency Stop button from Quick Actions
    old_button = '<button class="btn danger" onclick="emergencyStop()">🛑 Emergency Stop</button>'
    
    if old_button in html:
        html = html.replace(old_button, '')
        print("[OK] Removed Emergency Stop button")
    else:
        print("[SKIP] Button not found or already removed")
    
    # Remove the emergencyStop function
    old_function = '''        function emergencyStop() {
            if (confirm('⚠️ This will stop ALL bots. Continue?')) {
                // Call OpenClaw API to kill all crons
                const response = await fetch('/api/emergency-stop', { method: 'POST' });
                alert(response.ok ? 'All bots stopped' : 'Failed to stop bots');
            }
        }'''
    
    if 'function emergencyStop()' in html:
        # Find and remove the function (it spans multiple lines)
        import re
        pattern = r'function emergencyStop\(\) \{[\s\S]*?\n        \}'
        html = re.sub(pattern, '', html)
        print("[OK] Removed emergencyStop() function")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Emergency Stop button removed for security")
    print("\nReason: Dashboard is on public GitHub Pages")
    print("Anyone with the URL could have clicked it")
    print("\nDashboard is now READ-ONLY (monitoring only)")
    print("\nTo control bots, use OpenClaw CLI directly:")
    print("  openclaw cron list")
    print("  openclaw cron kill <id>")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Remove Emergency Stop - security risk on public site' && git push")

if __name__ == "__main__":
    main()
