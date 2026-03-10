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
            timeout=30
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
            timeout=30
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

def get_clip_empire_stats():
    """Read Clip Empire channel stats + creator profiles from the DB and config."""
    import sqlite3 as _sq
    DB = os.path.join(WORKSPACE, 'ventures', 'clip_empire', 'data', 'clip_empire.db')
    SOURCES_PATH = os.path.join(WORKSPACE, 'ventures', 'clip_empire', 'engine', 'config', 'sources.py')

    # Channel niche labels
    NICHE_MAP = {
        'arc_highlightz': 'Gaming',
        'fomo_highlights': 'Gaming',
        'viral_recaps': 'Gaming',
        'market_meltdowns': 'Finance',
        'crypto_confessions': 'Finance',
        'rich_or_ruined': 'Finance',
        'startup_graveyard': 'Business',
        'self_made_clips': 'Business',
        'ai_did_what': 'Tech/AI',
        'gym_moments': 'Fitness',
        'kitchen_chaos': 'Food',
        'cases_unsolved': 'True Crime',
        'unfiltered_clips': 'Misc',
    }

    # Creator-to-channel mapping (key creators only)
    CREATOR_MAP = {
        'arc_highlightz': ['Tfue', 'Cloakzy'],
        'fomo_highlights': ['Shroud', 'Nickmercs', 'TimTheTatman'],
        'viral_recaps': ['Moistcr1tikal', 'HasanAbi', 'Ludwig'],
        'market_meltdowns': ['PatrickBoyle', 'WSMillennial', 'Coffeezilla', 'RareLiquid'],
    }

    channels = []
    today = datetime.now().strftime('%Y-%m-%d')

    try:
        conn = _sq.connect(DB)
        rows = conn.execute(
            "SELECT channel_name, status, daily_target FROM channels ORDER BY status DESC, channel_name"
        ).fetchall()

        for ch_name, status, daily_target in rows:
            niche = NICHE_MAP.get(ch_name, 'Unknown')
            # Jobs today (succeeded + queued)
            today_count = conn.execute(
                """SELECT COUNT(*) FROM publish_jobs
                   WHERE channel_name=? AND date(created_at)=?
                   AND status IN ('succeeded','queued','running')""",
                (ch_name, today)
            ).fetchone()[0]

            # Last succeeded job
            last_row = conn.execute(
                """SELECT caption_text, created_at FROM publish_jobs
                   WHERE channel_name=? AND status='succeeded'
                   ORDER BY created_at DESC LIMIT 1""",
                (ch_name,)
            ).fetchone()
            last_title = last_row[0][:50] if last_row else None
            last_ts = last_row[1][:16] if last_row else None

            # Queued jobs
            queued = conn.execute(
                "SELECT COUNT(*) FROM publish_jobs WHERE channel_name=? AND status='queued'",
                (ch_name,)
            ).fetchone()[0]

            channels.append({
                'name': ch_name,
                'niche': niche or NICHE_MAP.get(ch_name, 'Unknown'),
                'status': status,
                'daily_target': daily_target or 0,
                'today_count': today_count,
                'queued': queued,
                'last_title': last_title,
                'last_ts': last_ts,
                'creators': CREATOR_MAP.get(ch_name, []),
            })
        conn.close()
    except Exception as e:
        print(f"[WARN] Clip Empire DB read failed: {e}")

    active = [c for c in channels if c['status'] == 'active']
    total_today = sum(c['today_count'] for c in channels)
    total_queued = sum(c['queued'] for c in channels)
    total_target = sum(c['daily_target'] for c in active)

    return {
        'channels': channels,
        'active_count': len(active),
        'total_count': len(channels),
        'total_today': total_today,
        'total_queued': total_queued,
        'total_target': total_target,
        # Legacy keys kept for backwards compat
        'arc_clips_today': next((c['today_count'] for c in channels if c['name'] == 'arc_highlightz'), 0),
        'rage_clips_today': next((c['today_count'] for c in channels if c['name'] == 'fomo_highlights'), 0),
        'viral_clips_today': next((c['today_count'] for c in channels if c['name'] == 'viral_recaps'), 0),
    }


def get_content_engine_stats():
    """Wrapper — now delegates to Clip Empire DB reader."""
    try:
        return get_clip_empire_stats()
    except Exception as e:
        print(f"[WARN] Could not get content engine stats: {e}")
        return {
            'channels': [],
            'active_count': 0,
            'total_count': 0,
            'total_today': 0,
            'total_queued': 0,
            'total_target': 0,
            'arc_clips_today': 0,
            'arc_views': 0,
            'arc_subs': 0,
            'rage_clips_today': 0,
            'rage_views': 0,
            'rage_subs': 0,
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
        "clip_empire": {
            "channels": content_stats.get('channels', []),
            "active_count": content_stats.get('active_count', 0),
            "total_count": content_stats.get('total_count', 0),
            "total_today": content_stats.get('total_today', 0),
            "total_queued": content_stats.get('total_queued', 0),
            "total_target": content_stats.get('total_target', 0),
        },
        "stats": {
            **stats,
            'arcClipsToday': content_stats.get('arc_clips_today', 0),
            'arcViews': content_stats.get('arc_views', 0),
            'arcSubs': content_stats.get('arc_subs', 42),
            'rageClipsToday': content_stats.get('rage_clips_today', 0),
            'rageViews': content_stats.get('rage_views', 0),
            'rageSubs': content_stats.get('rage_subs', 38),
            'viralClipsToday': content_stats.get('viral_clips_today', 0),
            'viralViews': content_stats.get('viral_views', 0),
            'viralSubs': content_stats.get('viral_subs', 0),
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
