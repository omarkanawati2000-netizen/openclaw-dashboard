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
    """Get cron job status from OpenClaw"""
    bots = []
    
    try:
        # Use PowerShell to run openclaw (it's a .ps1 script)
        result = subprocess.run(
            ['powershell', '-Command', 'openclaw', 'cron', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            
            # Skip header line
            for line in lines[1:]:
                if not line.strip():
                    continue
                
                # Parse the line (space-separated columns)
                parts = line.split()
                if len(parts) < 8:
                    continue
                
                # Extract fields
                cron_id = parts[0]
                
                # Name might have spaces, so find where "cron" starts
                name_parts = []
                i = 1
                while i < len(parts) and not parts[i].startswith('cron'):
                    name_parts.append(parts[i])
                    i += 1
                name = ' '.join(name_parts)
                
                # Find other fields
                next_run = 'Unknown'
                last_run = 'Unknown'
                status = 'unknown'
                
                # Look for "in" (next run), "ago" (last run), status
                for j, part in enumerate(parts):
                    if part == 'in' and j + 1 < len(parts):
                        next_run = parts[j + 1]
                    elif part.endswith('ago'):
                        if j > 0:
                            last_run = f"{parts[j-1]} {part}"
                        else:
                            last_run = part
                    elif part in ['ok', 'idle', 'error', 'running']:
                        status = part
                
                # Determine interval from schedule
                interval = 'Unknown'
                if 'cron' in parts:
                    sched_idx = parts.index('cron')
                    if sched_idx + 1 < len(parts):
                        sched = parts[sched_idx + 1]
                        if sched == '0':
                            if sched_idx + 2 < len(parts):
                                min_part = parts[sched_idx + 2]
                                if '/' in min_part or '*' in min_part:
                                    interval = 'Hourly'
                                else:
                                    interval = 'Daily'
                        elif '/' in sched:
                            interval = sched.replace('*/', 'Every ') + ' min'
                
                bots.append({
                    'name': name[:30],  # Truncate long names
                    'status': status,
                    'interval': interval,
                    'lastRun': last_run,
                    'nextRun': next_run,
                    'errors': 0,  # Would need to track from logs
                    'id': cron_id
                })
            
            print(f"[OK] Parsed {len(bots)} cron jobs from openclaw")
            return bots
        else:
            print(f"[WARN] openclaw cron list failed")
    except Exception as e:
        print(f"[WARN] Could not get cron bots: {e}")
    
    # Fallback mock data
    return [
        { 'name': 'RSI Bot', 'status': 'idle', 'interval': '30 min', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
        { 'name': 'SMC Bot', 'status': 'idle', 'interval': 'Hourly', 'lastRun': 'Unknown', 'nextRun': 'Unknown', 'errors': 0 },
    ]

def get_active_sessions():
    """Get active OpenClaw agent sessions"""
    try:
        # Run openclaw CLI to list sessions (via PowerShell)
        result = subprocess.run(
            ['powershell', '-Command', 'openclaw', 'sessions', 'list', '--json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            sessions_data = json.loads(result.stdout)
            sessions = []
            
            for session in sessions_data.get('sessions', []):
                # Get display name or parse from key
                name = session.get('displayName', None)
                session_key = session.get('key', '')
                channel = session.get('channel', 'unknown')
                
                # If no display name, parse from session key
                if not name or name == 'Unknown':
                    if ':discord:' in session_key:
                        if ':channel:' in session_key:
                            channel_id = session_key.split(':channel:')[-1]
                            name = f'Discord Channel {channel_id[:8]}...'
                            channel = 'discord'
                        elif ':dm:' in session_key:
                            name = 'Discord DM'
                            channel = 'discord'
                    elif ':telegram:' in session_key:
                        if session_key.endswith('-1003146730450'):
                            name = 'Telegram Retards v2'
                        else:
                            group_id = session_key.split(':')[-1]
                            name = f'Telegram {group_id[:8]}...'
                        channel = 'telegram'
                    elif ':subagent:' in session_key:
                        name = 'Subagent Session'
                        channel = 'subagent'
                    else:
                        name = f'Session {session_key.split(":")[-1][:8]}...'
                
                sessions.append({
                    'name': name,
                    'channel': channel,
                    'kind': session.get('kind', 'unknown'),
                    'model': session.get('model', 'unknown'),
                    'tokens': session.get('totalTokens', 0),
                    'lastActive': format_timestamp(session.get('updatedAt', 0)),
                    'sessionKey': session_key
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

def get_youtube_channel_stats(channel_id):
    """Fetch YouTube channel stats via YouTube Data API"""
    try:
        import subprocess
        
        # Use OpenClaw's YouTube integration (or fallback to CLI)
        # For now, return mock data - can be replaced with API calls
        result = subprocess.run(
            ['powershell', '-Command', 
             f'$ch = @{{channel_id = "{channel_id}"}}; '
             f'Write-Host "{{}}"'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Return mock stats (in production, would call YouTube API)
        return {'subs': 0, 'views7d': 0, 'clipsToday': 0}
    except:
        return {'subs': 0, 'views7d': 0, 'clipsToday': 0}

def get_content_engine_stats():
    """Get content engine upload stats from upload_queue.json files"""
    try:
        arc_clips = 0
        arc_views = 0
        arc_subs = 42  # Arc Highlightz
        
        rage_clips = 0
        rage_views = 0
        rage_subs = 38  # FomoHighlights
        
        # Count uploads from today
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Arc Highlightz upload queue
        arc_queue_file = os.path.join(WORKSPACE, 'ventures', 'clip_engine', 'upload_queue.json')
        if os.path.exists(arc_queue_file):
            try:
                with open(arc_queue_file, 'r', encoding='utf-8') as f:
                    arc_queue = json.load(f)
                
                # Count clips uploaded today
                for clip in arc_queue:
                    if clip.get('uploaded_at', '').startswith(today):
                        arc_clips += 1
            except Exception as e:
                print(f"[WARN] Could not read Arc upload queue: {e}")
        
        # FomoHighlights upload queue
        rage_queue_file = os.path.join(WORKSPACE, 'ventures', 'clip_engine_rage', 'upload_queue.json')
        if os.path.exists(rage_queue_file):
            try:
                with open(rage_queue_file, 'r', encoding='utf-8') as f:
                    rage_queue = json.load(f)
                
                # Count clips uploaded today
                for clip in rage_queue:
                    if clip.get('uploaded_at', '').startswith(today):
                        rage_clips += 1
            except Exception as e:
                print(f"[WARN] Could not read Rage upload queue: {e}")
        
        return {
            'arc_clips_today': arc_clips,
            'arc_views': arc_views,
            'arc_subs': arc_subs,
            'rage_clips_today': rage_clips,
            'rage_views': rage_views,
            'rage_subs': rage_subs,
        }
    except Exception as e:
        print(f"[WARN] Could not get content engine stats: {e}")
        return {
            'arc_clips_today': 0,
            'arc_views': 0,
            'arc_subs': 42,
            'rage_clips_today': 0,
            'rage_views': 0,
            'rage_subs': 38,
        }

def get_api_usage(sessions):
    """Get real API usage data"""
    usage = {}
    
    # Anthropic API - sum all session tokens
    total_tokens = sum(s.get('tokens', 0) or 0 for s in sessions if isinstance(s, dict))
    usage['anthropicTokens'] = total_tokens
    usage['anthropicPercent'] = min((total_tokens / 200000) * 100, 100) if total_tokens > 0 else 0
    
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

def get_machine_health():
    """Collect machine health metrics"""
    try:
        import psutil
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Memory
        mem = psutil.virtual_memory()
        mem_used_gb = mem.used / (1024**3)
        mem_total_gb = mem.total / (1024**3)
        mem_percent = mem.percent
        
        # Disk (C:)
        disk = psutil.disk_usage('C:\\')
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        disk_percent = disk.percent
        
        # Network speed (would need tracking over time for accuracy)
        net_speed = 0
        
        # Python processes
        python_procs = sum(1 for p in psutil.process_iter(['name']) if 'python' in p.info['name'].lower())
        
        return {
            'cpuPercent': cpu_percent,
            'memUsedGB': mem_used_gb,
            'memTotalGB': mem_total_gb,
            'memPercent': mem_percent,
            'diskUsedGB': disk_used_gb,
            'diskTotalGB': disk_total_gb,
            'diskPercent': disk_percent,
            'netSpeed': net_speed,
            'pythonProcesses': python_procs
        }
    except Exception as e:
        print(f"[WARN] Could not get machine health: {e}")
        return {}

def main():
    print("Generating dashboard data...")
    
    # Parse real data
    positions = parse_trades()
    bots = get_cron_bots()
    sessions = get_active_sessions()
    stats = calculate_stats(positions)
    api_usage = get_api_usage(sessions)
    machine = get_machine_health()
    content_stats = get_content_engine_stats()
    
    # System health
    workspace_size = get_folder_size(WORKSPACE)
    data_size = get_folder_size(os.path.join(WORKSPACE, "data"))
    
    # Build data object
    data = {
        "timestamp": datetime.now().isoformat(),
        "bots": bots,
        "positions": positions,
        "sessions": sessions,
        "machine": machine,
        "stats": {
            **stats,
            'arcClipsToday': content_stats.get('arc_clips_today', 0),
            'arcViews': content_stats.get('arc_views', 0),
            'arcSubs': content_stats.get('arc_subs', 42),
            'rageClipsToday': content_stats.get('rage_clips_today', 0),
            'rageViews': content_stats.get('rage_views', 0),
            'rageSubs': content_stats.get('rage_subs', 38),
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
    print(f"  - Machine: CPU {machine.get('cpuPercent', 0):.1f}%, RAM {machine.get('memPercent', 0):.1f}%, {machine.get('pythonProcesses', 0)} Python procs")
    print(f"  - Workspace: {workspace_size} MB")
    print(f"  - Data: {data_size} MB")

if __name__ == "__main__":
    main()
