#!/usr/bin/env python3
"""
OpenClaw Dashboard - GitHub Pages Deployment

GitHub Push Instructions for OpenClaw Agents:
============================================

Your GitHub username: omarkanawati2000-netizen
Auth method: Git Credential Manager (browser popup)

Standard Push Workflow:
-----------------------
1. Create repo on GitHub first (via API or manually on github.com/new)
2. Initialize local git repo: git init
3. Add files: git add .
4. Commit: git commit -m "Initial commit"
5. Add remote: git remote add origin https://github.com/omarkanawati2000-netizen/<repo>.git
6. Push: git push -u origin master (triggers browser popup for auth)

For Automated Pushes:
--------------------
Extract your Git credential token:
  echo "protocol=https`nhost=github.com`n" | git credential fill

This returns your OAuth token (starts with gho_).

Use the token in Python (see code below).
"""

import requests
import subprocess
import os
import sys

GITHUB_USERNAME = "omarkanawati2000-netizen"
REPO_NAME = "openclaw-dashboard"

def get_git_token():
    """Extract Git credential token via PowerShell"""
    try:
        # Run git credential fill to get token
        result = subprocess.run(
            ['powershell', '-Command', 'echo "protocol=https`nhost=github.com`n" | git credential fill'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse output for password (token)
            for line in result.stdout.split('\n'):
                if line.startswith('password='):
                    token = line.split('=', 1)[1].strip()
                    print(f"[OK] Got Git token: {token[:10]}...")
                    return token
        
        print("[ERROR] Could not extract Git token")
        return None
    except Exception as e:
        print(f"[ERROR] Token extraction failed: {e}")
        return None

def create_github_repo(token):
    """Create GitHub repository via API"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": REPO_NAME,
        "description": "OpenClaw automation infrastructure control center dashboard",
        "private": False
    }
    
    print(f"Creating repo: {REPO_NAME}...")
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        print(f"[OK] Repo created: {response.json()['html_url']}")
        return True
    elif response.status_code == 422:
        print("[INFO] Repo already exists")
        return True
    else:
        print(f"[ERROR] Failed to create repo: {response.status_code}")
        print(response.text)
        return False

def git_push(token):
    """Initialize git and push to GitHub"""
    os.chdir(os.path.dirname(__file__))
    
    # Check if git repo exists
    if not os.path.exists('.git'):
        print("Initializing git repo...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit - OpenClaw Dashboard'], check=True)
    
    # Add remote with token embedded
    remote_url = f"https://{token}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    
    # Remove existing remote if any
    subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True)
    
    # Add new remote
    print("Adding remote...")
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
    
    # Push
    print("Pushing to GitHub...")
    result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], capture_output=True, text=True)
    
    if result.returncode == 0 or 'up-to-date' in result.stderr.lower():
        print("[OK] Pushed to GitHub")
        return True
    else:
        # Try pushing to main instead
        print("Trying 'main' branch...")
        result = subprocess.run(['git', 'branch', '-M', 'main'], capture_output=True)
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Pushed to GitHub (main branch)")
            return True
        
        print(f"[ERROR] Push failed: {result.stderr}")
        return False

def enable_github_pages(token):
    """Enable GitHub Pages via API"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Try both master and main
    for branch in ['master', 'main']:
        data = {
            "source": {
                "branch": branch,
                "path": "/"
            }
        }
        
        print(f"Enabling GitHub Pages (branch: {branch})...")
        response = requests.post(
            f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages",
            headers=headers,
            json=data
        )
        
        if response.status_code in [201, 200]:
            pages_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
            print(f"[OK] GitHub Pages enabled!")
            print(f"URL: {pages_url}")
            return pages_url
        elif response.status_code == 409:
            pages_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
            print(f"[INFO] GitHub Pages already enabled")
            print(f"URL: {pages_url}")
            return pages_url
    
    print(f"[ERROR] Failed to enable Pages: {response.status_code}")
    print(response.text)
    return None

def main():
    print("=" * 60)
    print("OpenClaw Dashboard - GitHub Pages Deployment")
    print("=" * 60)
    print()
    
    # Step 1: Get Git token
    token = get_git_token()
    if not token:
        print("\n[ERROR] Cannot proceed without Git token")
        print("\nManual steps:")
        print("1. Run: echo \"protocol=https`nhost=github.com`n\" | git credential fill")
        print("2. Copy the password= line (your token)")
        print("3. Set TOKEN environment variable and re-run")
        sys.exit(1)
    
    # Step 2: Create repo
    if not create_github_repo(token):
        print("\n[ERROR] Repo creation failed")
        sys.exit(1)
    
    # Step 3: Push code
    if not git_push(token):
        print("\n[ERROR] Git push failed")
        sys.exit(1)
    
    # Step 4: Enable Pages
    url = enable_github_pages(token)
    
    if url:
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("=" * 60)
        print(f"Live site: {url}")
        print("\nNote: GitHub Pages may take 1-2 minutes to build and deploy.")
    else:
        print("\n[WARNING] Deployment succeeded but Pages setup failed")
        print("Enable manually:")
        print(f"1. Go to https://github.com/{GITHUB_USERNAME}/{REPO_NAME}/settings/pages")
        print("2. Source: Deploy from a branch")
        print("3. Branch: main (or master) / (root)")
        print("4. Save")

if __name__ == "__main__":
    main()
