#!/usr/bin/env python3
"""Add Machine Health panel to dashboard"""

import subprocess
import psutil
import json
from datetime import datetime

HTML_FILE = "index.html"

# Machine Health panel HTML
MACHINE_HEALTH_HTML = '''
            <!-- Machine Health -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">💻 Machine Health</div>
                    <div class="panel-badge" id="machineStatus">Good</div>
                </div>
                
                <div class="panel-content">
                    <div class="health-metric">
                        <div class="metric-header">
                            <span class="metric-name">CPU Usage</span>
                            <span class="metric-value" id="cpuUsage">0%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="cpuBar" style="width: 0%"></div>
                        </div>
                    </div>

                    <div class="health-metric">
                        <div class="metric-header">
                            <span class="metric-name">Memory (RAM)</span>
                            <span class="metric-value" id="memUsage">0 GB / 0 GB</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="memBar" style="width: 0%"></div>
                        </div>
                    </div>

                    <div class="health-metric">
                        <div class="metric-header">
                            <span class="metric-name">Disk (C:)</span>
                            <span class="metric-value" id="diskUsage">0 GB / 0 GB</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="diskBar" style="width: 0%"></div>
                        </div>
                    </div>

                    <div class="health-metric">
                        <div class="metric-header">
                            <span class="metric-name">Network</span>
                            <span class="metric-value" id="netUsage">0 KB/s</span>
                        </div>
                    </div>

                    <div class="health-metric">
                        <div class="metric-header">
                            <span class="metric-name">Python Processes</span>
                            <span class="metric-value" id="pythonProcs">0</span>
                        </div>
                    </div>
                </div>
            </div>'''

# CSS for machine health metrics
MACHINE_HEALTH_CSS = '''
        /* Machine Health metrics */
        .health-metric {
            margin-bottom: 1rem;
        }

        .metric-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .metric-name {
            font-weight: 600;
            font-size: 0.9rem;
        }

        .metric-value {
            color: var(--orange);
            font-weight: 600;
            font-size: 0.9rem;
        }'''

# JavaScript to render machine health
MACHINE_HEALTH_JS = '''
        function renderMachineHealth() {
            const data = dashboardData || mockData;
            const machine = data.machine || {};
            
            // CPU
            const cpuPercent = machine.cpuPercent || 0;
            document.getElementById('cpuUsage').textContent = `${cpuPercent.toFixed(1)}%`;
            document.getElementById('cpuBar').style.width = `${cpuPercent}%`;
            
            // Memory
            const memUsed = machine.memUsedGB || 0;
            const memTotal = machine.memTotalGB || 0;
            const memPercent = machine.memPercent || 0;
            document.getElementById('memUsage').textContent = `${memUsed.toFixed(1)} GB / ${memTotal.toFixed(1)} GB`;
            document.getElementById('memBar').style.width = `${memPercent}%`;
            
            // Disk
            const diskUsed = machine.diskUsedGB || 0;
            const diskTotal = machine.diskTotalGB || 0;
            const diskPercent = machine.diskPercent || 0;
            document.getElementById('diskUsage').textContent = `${diskUsed.toFixed(0)} GB / ${diskTotal.toFixed(0)} GB`;
            document.getElementById('diskBar').style.width = `${diskPercent}%`;
            
            // Network
            const netSpeed = machine.netSpeed || 0;
            let netDisplay = netSpeed < 1024 ? `${netSpeed.toFixed(0)} KB/s` : `${(netSpeed/1024).toFixed(1)} MB/s`;
            document.getElementById('netUsage').textContent = netDisplay;
            
            // Python processes
            const pythonProcs = machine.pythonProcesses || 0;
            document.getElementById('pythonProcs').textContent = pythonProcs;
            
            // Overall status
            const status = (cpuPercent > 80 || memPercent > 90 || diskPercent > 90) ? 'Warning' : 'Good';
            document.getElementById('machineStatus').textContent = status;
        }
'''

def get_machine_health():
    """Collect machine health metrics"""
    try:
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
        
        # Network (current speed estimate)
        net = psutil.net_io_counters()
        net_speed = 0  # Would need to track over time for real speed
        
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
            'pythonProcesses': python_procs,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"[WARN] Could not get machine health: {e}")
        return {}

def main():
    print("Adding Machine Health panel...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add panel HTML after System Health panel
    if '<!-- Machine Health -->' not in html:
        html = html.replace(
            '<!-- Performance Chart (placeholder) -->',
            MACHINE_HEALTH_HTML + '\n\n            <!-- Performance Chart (placeholder) -->'
        )
        print("[OK] Added Machine Health panel HTML")
    
    # Add CSS
    if '/* Machine Health metrics */' not in html:
        html = html.replace(
            '        /* Mobile: stack sessions */',
            MACHINE_HEALTH_CSS + '\n\n        /* Mobile: stack sessions */'
        )
        print("[OK] Added Machine Health CSS")
    
    # Add JavaScript
    if 'function renderMachineHealth()' not in html:
        html = html.replace(
            '        function renderApiUsage() {',
            MACHINE_HEALTH_JS + '\n        function renderApiUsage() {'
        )
        print("[OK] Added renderMachineHealth() function")
    
    # Add to refreshDashboard
    if 'renderMachineHealth();' not in html:
        html = html.replace(
            'renderSessions();',
            'renderSessions();\n            renderMachineHealth();'
        )
        print("[OK] Added renderMachineHealth() to refresh")
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Test collecting machine health
    print("\n[INFO] Testing machine health collection...")
    health = get_machine_health()
    if health:
        print(f"  CPU: {health['cpuPercent']:.1f}%")
        print(f"  RAM: {health['memUsedGB']:.1f} GB / {health['memTotalGB']:.1f} GB ({health['memPercent']:.1f}%)")
        print(f"  Disk: {health['diskUsedGB']:.0f} GB / {health['diskTotalGB']:.0f} GB ({health['diskPercent']:.1f}%)")
        print(f"  Python processes: {health['pythonProcesses']}")
    
    print(f"\n[OK] Machine Health panel added")
    print("\nNext: Update generate_data.py to include machine health")
    print("Then deploy:")
    print("git add index.html generate_data.py && git commit -m 'Add Machine Health panel' && git push")

if __name__ == "__main__":
    # Check if psutil is available
    try:
        import psutil
    except ImportError:
        print("[ERROR] psutil not installed")
        print("Install with: pip install psutil")
        exit(1)
    
    main()
