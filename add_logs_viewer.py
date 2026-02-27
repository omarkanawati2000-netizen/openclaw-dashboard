#!/usr/bin/env python3
"""Add Logs Viewer modal to OpenClaw Dashboard"""

HTML_FILE = "index.html"

# Modal HTML
MODAL_HTML = '''
    <!-- Logs Viewer Modal -->
    <div id="logsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>📋 Logs Viewer</h2>
                <span class="modal-close" onclick="closeLogsModal()">&times;</span>
            </div>
            <div class="modal-body">
                <p>Logs viewer coming soon</p>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;">
                    This feature will allow you to view and filter logs from all your bots, trading systems, and automation tasks.
                </p>
            </div>
            <div class="modal-footer">
                <button class="btn primary" onclick="closeLogsModal()">OK</button>
            </div>
        </div>
    </div>
'''

# Modal CSS
MODAL_CSS = '''
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            animation: fadeIn 0.2s;
        }

        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background: var(--bg-panel);
            border: 1px solid var(--orange);
            border-radius: 8px;
            max-width: 500px;
            width: 90%;
            animation: slideIn 0.3s;
        }

        @keyframes slideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .modal-header {
            padding: 1.5rem;
            border-bottom: 1px solid #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h2 {
            margin: 0;
            font-size: 1.5rem;
            color: var(--orange);
        }

        .modal-close {
            font-size: 2rem;
            color: var(--text-dim);
            cursor: pointer;
            line-height: 1;
            transition: color 0.2s;
        }

        .modal-close:hover {
            color: var(--orange);
        }

        .modal-body {
            padding: 2rem 1.5rem;
        }

        .modal-body p {
            margin: 0;
            font-size: 1.1rem;
        }

        .modal-footer {
            padding: 1rem 1.5rem;
            border-top: 1px solid #333;
            text-align: right;
        }

        .modal-footer .btn {
            min-width: 100px;
        }
'''

# Modal JavaScript
MODAL_JS = '''
        function showLogsModal() {
            document.getElementById('logsModal').classList.add('show');
        }

        function closeLogsModal() {
            document.getElementById('logsModal').classList.remove('show');
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('logsModal');
            if (event.target == modal) {
                closeLogsModal();
            }
        }

        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeLogsModal();
            }
        });
'''

def main():
    print("Adding Logs Viewer modal...")
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add modal HTML before closing body tag
    if 'id="logsModal"' not in html:
        html = html.replace('</body>', MODAL_HTML + '\n</body>')
        print("[OK] Added modal HTML")
    else:
        print("[SKIP] Modal HTML already exists")
    
    # 2. Add modal CSS
    if '.modal {' not in html:
        html = html.replace('        /* Enhanced Mobile Responsive */', 
                           MODAL_CSS + '\n        /* Enhanced Mobile Responsive */')
        print("[OK] Added modal CSS")
    else:
        print("[SKIP] Modal CSS already exists")
    
    # 3. Add modal JavaScript
    if 'function showLogsModal()' not in html:
        html = html.replace('        // Mobile: collapsible panels',
                           MODAL_JS + '\n        // Mobile: collapsible panels')
        print("[OK] Added modal JavaScript")
    else:
        print("[SKIP] Modal JavaScript already exists")
    
    # 4. Update View Logs button to show modal
    html = html.replace('onclick="alert(\'Logs viewer coming soon\')"',
                       'onclick="showLogsModal()"')
    print("[OK] Updated View Logs button")
    
    # Write updated HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n[OK] Added Logs Viewer modal to {HTML_FILE}")
    print("\nFeatures:")
    print("- Click 'View Logs' button to show modal")
    print("- Close with X button, OK button, clicking outside, or Escape key")
    print("- Smooth animations")
    print("- Mobile-friendly")
    print("\nDeploy:")
    print("git add index.html && git commit -m 'Add Logs Viewer modal' && git push")

if __name__ == "__main__":
    main()
