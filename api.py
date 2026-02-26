#!/usr/bin/env python3
"""
OpenClaw Dashboard API
Provides JSON endpoints for real data integration
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import re
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app)  # Allow requests from GitHub Pages

WORKSPACE = r"C:\Users\kanaw\.openclaw\workspace"

@app.route('/api/positions', methods=['GET'])
def get_positions():
    """Parse trades.md for open positions"""
    try:
        trades_file = os.path.join(WORKSPACE, "memory", "trades.md")
        if not os.path.exists(trades_file):
            return jsonify({"positions": [], "error": "trades.md not found"})
        
        with open(trades_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        positions = []
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
                        'size': None,
                        'entry': None,
                        'sl': None,
                        'tp': None,
                        'strategy': None
                    }
            elif current_pos and line.startswith('- **'):
                # Parse position details
                if 'Strategy:' in line:
                    current_pos['strategy'] = line.split('**')[1].strip()
                elif 'Size:' in line:
                    size_str = line.split('**')[2].strip()
                    try:
                        current_pos['size'] = float(size_str)
                    except:
                        pass
                elif 'Entry:' in line:
                    entry_str = line.split('$')[1].strip()
                    try:
                        current_pos['entry'] = float(entry_str)
                    except:
                        pass
                elif 'Stop Loss:' in line:
                    sl_str = line.split('$')[1].strip()
                    try:
                        current_pos['sl'] = float(sl_str)
                    except:
                        pass
                elif 'Take Profit:' in line:
                    tp_str = line.split('$')[1].strip()
                    try:
                        current_pos['tp'] = float(tp_str)
                    except:
                        pass
        
        if current_pos:
            positions.append(current_pos)
        
        return jsonify({
            "positions": positions,
            "count": len(positions),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e), "positions": []})

@app.route('/api/system', methods=['GET'])
def get_system_health():
    """Get system health metrics"""
    try:
        # Calculate workspace size
        workspace_size = get_folder_size(WORKSPACE) / (1024 * 1024)  # MB
        data_size = get_folder_size(os.path.join(WORKSPACE, "data")) / (1024 * 1024)  # MB
        
        return jsonify({
            "workspace_size_mb": round(workspace_size, 2),
            "data_size_mb": round(data_size, 2),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/cron', methods=['GET'])
def get_cron_status():
    """Get OpenClaw cron job status"""
    try:
        # Run openclaw cron list
        result = subprocess.run(
            ['openclaw', 'cron', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return jsonify({"error": "openclaw cron list failed", "bots": []})
        
        # Parse output (you'll need to adapt this to actual format)
        bots = []
        # TODO: Parse openclaw cron list output
        
        return jsonify({
            "bots": bots,
            "count": len(bots),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({"error": str(e), "bots": []})

def get_folder_size(folder):
    """Calculate folder size in bytes"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
    except:
        pass
    return total_size

if __name__ == '__main__':
    print("OpenClaw Dashboard API")
    print("======================")
    print("Starting server on http://localhost:5000")
    print()
    print("Endpoints:")
    print("  GET /api/positions - Trading positions from trades.md")
    print("  GET /api/system    - System health metrics")
    print("  GET /api/cron      - Cron job status")
    print()
    app.run(host='0.0.0.0', port=5000, debug=True)
