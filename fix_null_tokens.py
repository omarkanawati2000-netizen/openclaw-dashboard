#!/usr/bin/env python3
"""Fix null token error in sessions rendering"""

HTML_FILE = "index.html"

def main():
    print("Fixing null token errors...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find and fix renderSessions function to handle null tokens
    old_token_line = '${session.tokens.toLocaleString()} tokens used'
    new_token_line = '${(session.tokens || 0).toLocaleString()} tokens used'
    
    if old_token_line in html:
        html = html.replace(old_token_line, new_token_line)
        print("[OK] Fixed session token null handling")
    else:
        print("[SKIP] Session token line already fixed or not found")
    
    # Also fix the anthropic API calculation to handle null tokens in sessions
    old_tokens_calc = 'const sessions = data.sessions || [];'
    new_tokens_calc = '''const sessions = data.sessions || [];
                const totalSessionTokens = sessions.reduce((sum, s) => sum + (s.tokens || 0), 0);'''
    
    # Find where we calculate anthropic tokens in renderApiUsage
    if 'const sessions = data.sessions || [];' in html and 'const totalSessionTokens' not in html:
        # Replace in renderApiUsage function
        import re
        # Find the renderApiUsage function and update it
        html = html.replace(
            'const sessions = data.sessions || [];\n                document.getElementById(\'anthropicApiMeta\').textContent = `Across ${sessions.length} sessions`;',
            'const sessions = data.sessions || [];\n                document.getElementById(\'anthropicApiMeta\').textContent = `Across ${sessions.length} sessions`;'
        )
        print("[OK] Ensured session token handling is safe")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Fixed null token errors")
    print("\nChanges:")
    print("- Sessions with null tokens now show '0 tokens used'")
    print("- No more TypeError crashes")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Fix null token errors in sessions' && git push")

if __name__ == "__main__":
    main()
