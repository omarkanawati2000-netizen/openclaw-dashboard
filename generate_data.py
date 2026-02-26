#!/usr/bin/env python3
"""
Generate data.json for OpenClaw Dashboard
Run this periodically (e.g., via cron) to update dashboard with real data
"""

import json
import os
import re
from datetime import datetime
import subprocess

WORKSPACE = r"C:\Users\kanaw\.openclaw\workspace"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def parse_trades():
    """Parse trades.md for open positions"""
    positions = []
    
    try:
        trades_file = os.path.join(WORKSPACE, "memory", "trades.md")
        if not os.path.exists(trades_file):
            return positions
        
        with open(trades_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        current_pos = None
        
        for line in content.split('\n'):
            if line.startswith('## OPEN:'):
                # New position
                match = re.match(r'## OPEN: (\w+) (LONG|SHORT)', line)
                if match:
                    if current_pos:
                        positions.append(current_pos)
                    current_pos = {
                        'coin': match.group(1),
                        'direction': match.group(2),
                        'size': 0,
                        'entry': 0,
                        'sl': 0,
                        'tp': 0,
                        'strategy': 'Unknown',
                        'pnl': 0,
                        'pnlPercent': 0
                    }
            elif current_pos:
                # Parse position details
                if '**Strategy:**' in line:
                    current_pos['strategy'] = line.split('**Strategy:**')[1].strip().split('\n')[0]
                elif '**Size:**' in line:
                    try:
                        size_str = line.split('**Size:**')[1].strip().split('\n')[0]
                        current_pos['size'] = float(size_str)
                    except:
                        pass
                elif '**Entry:**' in line:
                    try:
                        entry_str = line.split('$')[1].strip().split('\n')[0]
                        current_pos['entry'] = float(entry_str)
                    except:
                        pass
                elif '**Stop Loss:**' in line:
                    try:
                        sl_str = line.split('$')[1].strip().split('\n')[0]
                        current_pos['sl'] = float(sl_str)
                    except:
                        pass
                elif '**Take Profit:**' in line:
                    try:
                        tp_str = line.split('$')[1].strip().split('\n')[0]
                        current_pos['tp'] = float(tp_str)
                    except:
                        pass
        
        if current_pos:
            positions.append(current_pos)
    
    except Exception as e:
        print(f"Error parsing trades: {e}")
    
    return positions

def get_folder_size(folder):
    """Calculate folder size in MB"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            # Skip large dirs
            if '.git' in dirpath or 'node_modules' in dirpath:
                continue
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    try:
                        total_size += os.path.getsize(filepath)
                    except:
                        pass
    except:
        pass
    return round(total_size / (1024 * 1024), 2)

def get_cron_bots():
    """Get cron job status (mock for now - can be enhanced)"""
    # TODO: Parse `openclaw cron list` output
    return [
        { 'name': 'RSI Bot', 'status': 'idle', 'interval': '30 min', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'SMC Bot', 'status': 'idle', 'interval': 'Hourly', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Arc Highlightz Clipper', 'status': 'idle', 'interval': '30 min', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'FomoHighlights Clipper', 'status': 'idle', 'interval': '30 min', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Content Health Monitor', 'status': 'idle', 'interval': 'Hourly', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Data Collector', 'status': 'idle', 'interval': 'Daily', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Morning Market Briefing', 'status': 'idle', 'interval': 'Daily 9AM', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Idea Generator', 'status': 'idle', 'interval': 'Weekly', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'Security Scan', 'status': 'idle', 'interval': 'Daily', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
    ]

def get_active_sessions():
    """Get active OpenClaw agent sessions"""
    try:
        # Run openclaw CLI to list sessions
        result = subprocess.run(
            ['openclaw', 'sessions', 'list', '--json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            sessions_data = json.loads(result.stdout)
            sessions = []
            
            for session in sessions_data.get('sessions', []):
                sessions.append({
                    'name': session.get('displayName', 'Unknown'),
                    'channel': session.get('channel', 'unknown'),
                    'kind': session.get('kind', 'unknown'),
                    'model': session.get('model', 'unknown'),
                    'tokens': session.get('totalTokens', 0),
                    'lastActive': format_timestamp(session.get('updatedAt', 0)),
                    'sessionKey': session.get('key', '')
                })
            
            return sessions
        else:
            print(f"[WARN] openclaw sessions list failed: {result.stderr}")
    except Exception as e:
        print(f"[WARN] Could not get sessions: {e}")
    
    # Fallback mock data
    return [
        { 'name': 'Discord #general', 'channel': 'discord', 'kind': 'group', 'model': 'claude-sonnet-4-5', 'tokens': 89000, 'lastActive': '2 min ago', 'sessionKey': 'agent:main:discord:channel:1468193294906425430' },
        { 'name': 'Telegram Retards v2', 'channel': 'telegram', 'kind': 'group', 'model': 'claude-sonnet-4-5', 'tokens': 45000, 'lastActive': '1 hour ago', 'sessionKey': 'agent:main:telegram:-1003146730450' },
    ]

def format_timestamp(ts_ms):
    """Format timestamp to relative time"""
    if not ts_ms:
        return 'Unknown'
    
    try:
        from datetime import datetime
        dt = datetime.fromtimestamp(ts_ms / 1000)
        now = datetime.now()
        diff = now - dt
        
        if diff.seconds < 60:
            return 'Just now'
        elif diff.seconds < 3600:
            return f'{diff.seconds // 60} min ago'
        elif diff.seconds < 86400:
            return f'{diff.seconds // 3600} hours ago'
        else:
            return f'{diff.days} days ago'
    except:
        return 'Unknown'

def calculate_stats(positions):
    """Calculate trading stats from positions"""
    if not positions:
        return {
            'dailyPnl': 0,
            'winRate': 0,
            'positionCount': 0,
            'totalRevenue': 0,
        }
    
    total_pnl = sum(p['pnl'] for p in positions)
    positive = sum(1 for p in positions if p['pnl'] > 0)
    win_rate = round((positive / len(positions)) * 100) if positions else 0
    
    return {
        'dailyPnl': round(total_pnl, 2),
        'winRate': win_rate,
        'positionCount': len(positions),
        'totalRevenue': 850,  # Mock - could track actual revenue
    }

def get_api_usage(sessions):
    """Get real API usage data"""
    usage = {}
    
    # Anthropic API - sum all session tokens
    total_tokens = sum(s.get('tokens', 0) for s in sessions)
    usage['anthropicTokens'] = total_tokens
    usage['anthropicPercent'] = min((total_tokens / 200000) * 100, 100)
    
    # YouTube API - try to get from quota file or config
    try:
        # Check if we track YouTube quota somewhere
        quota_file = os.path.join(WORKSPACE, 'ventures', 'clip_engine', 'youtube_quota.txt')
        if os.path.exists(quota_file):
            with open(quota_file, 'r') as f:
                usage['ytQuotaUsed'] = int(f.read().strip())
        else:
            usage['ytQuotaUsed'] = 0
    except:
        usage['ytQuotaUsed'] = 0
    
    # OpenAI API - estimate from usage (could integrate with OpenAI API)
    usage['openaiUsage'] = 15  # Mock for now
    
    # Hyperliquid - always "Good" unless we detect rate limiting
    usage['hyperliquidRate'] = 'Good'
    
    # Twitch API - would need to track API calls
    usage['twitchUsage'] = 'Unknown'
    
    return usage

def main():
    print("Generating dashboard data...")
    
    # Parse real data
    positions = parse_trades()
    bots = get_cron_bots()
    sessions = get_active_sessions()
    stats = calculate_stats(positions)
    api_usage = get_api_usage(sessions)
    
    # System health
    workspace_size = get_folder_size(WORKSPACE)
    data_size = get_folder_size(os.path.join(WORKSPACE, "data"))
    
    # Build data object
    data = {
        "timestamp": datetime.now().isoformat(),
        "bots": bots,
        "positions": positions,
        "sessions": sessions,
        "stats": {
            **stats,
            'arcClipsToday': 0,  # TODO: Count from Discord/logs
            'arcViews': 0,
            'arcSubs': 0,
            'rageClipsToday': 0,
            'rageViews': 0,
            'rageSubs': 0,
            'ytQuotaUsed': api_usage.get('ytQuotaUsed', 0),
            'openaiUsage': api_usage.get('openaiUsage', 15),
            'hyperliquidRate': api_usage.get('hyperliquidRate', 'Good'),
            'twitchUsage': api_usage.get('twitchUsage', 'Unknown'),
            'anthropicTokens': api_usage.get('anthropicTokens', 0),
            'anthropicPercent': api_usage.get('anthropicPercent', 0),
            'openclawRevenue': 0,
            'openclawClients': 0,
            'tradingRevenue': 850,
            'contentRevenue': 0,
            'monthlyTarget': 10000,
            'workspaceSize': workspace_size,
            'dataSize': data_size,
        }
    }
    
    # Write to file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[OK] Generated {OUTPUT_FILE}")
    print(f"  - {len(positions)} positions")
    print(f"  - {len(bots)} bots")
    print(f"  - {len(sessions)} sessions")
    print(f"  - API: {api_usage.get('anthropicTokens', 0):,} Anthropic tokens, {api_usage.get('ytQuotaUsed', 0)} YT quota")
    print(f"  - Workspace: {workspace_size} MB")
    print(f"  - Data: {data_size} MB")

if __name__ == "__main__":
    main()
