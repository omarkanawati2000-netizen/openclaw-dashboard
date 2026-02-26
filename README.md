# OpenClaw Dashboard

Comprehensive monitoring and control center for Omar's OpenClaw automation infrastructure.

## Features

### 🤖 Bot Status Panel
- Real-time status of all cron jobs (RSI Bot, SMC Bot, Clip Engines, etc.)
- Last run times, next run schedules
- Success/error tracking
- Quick action buttons

### 📈 Trading Dashboard
- Open positions with live P&L
- Daily performance metrics
- Win rate tracking
- Best/worst performers

### 🎬 Content Engine Stats
- Arc Highlightz YouTube channel metrics
- FomoHighlights YouTube channel metrics
- Upload queue status
- YouTube API quota monitoring

### 💰 Revenue Tracker
- Multiple income streams (OpenClaw business, trading, content)
- Monthly revenue targets with progress bars
- New client tracking
- Goal milestones

### ⚙️ System Health
- API quota monitoring (OpenAI, YouTube, Hyperliquid)
- Disk space usage
- Recent error logs
- System status indicators

### 🎯 Quick Actions Bar
- Refresh all data
- Open trading terminal
- View logs
- Emergency stop (kill all bots)

## Tech Stack

- **Single HTML file** with inline CSS/JS
- **No frameworks** - vanilla JavaScript for performance
- **Dark theme** - Bloomberg-inspired with orange accents
- **IBM Plex Mono** font
- **Auto-refresh** every 10 seconds
- **Fully responsive** (desktop + mobile)

## Deployment

### Automated (via Python)

```bash
python deploy.py
```

This will:
1. Extract your Git credential token
2. Create the GitHub repo (if needed)
3. Push the code
4. Enable GitHub Pages
5. Print the live URL

### Manual

```bash
# 1. Create repo on GitHub
gh repo create openclaw-dashboard --public

# 2. Push code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/omarkanawati2000-netizen/openclaw-dashboard.git
git push -u origin master

# 3. Enable Pages
Go to repo settings → Pages → Source: Deploy from branch → main/(root) → Save
```

## Live Site

**URL:** https://omarkanawati2000-netizen.github.io/openclaw-dashboard/

## Data Integration

**Current:** Mock data for all sections (MVP)

**Future:** Real integrations
- Parse `memory/trades.md` for trading positions
- Query OpenClaw cron status API
- Fetch Hyperliquid API data
- Query YouTube Analytics API
- Read system log files

## File Structure

```
openclaw_dashboard/
├── index.html (26KB single-file dashboard)
├── deploy.py (GitHub deployment script)
├── SPEC.md (original specification)
└── README.md (this file)
```

## Customization

### Update Mock Data

Edit the `mockData` object in `index.html`:

```javascript
const mockData = {
    bots: [ ... ],
    positions: [ ... ],
    stats: { ... }
};
```

### Add Real Data Integration

Replace mock data with API calls:

```javascript
async function fetchRealData() {
    // Fetch from OpenClaw API, Hyperliquid, YouTube, etc.
    const response = await fetch('your-api-endpoint');
    const data = await response.json();
    return data;
}
```

### Styling

All CSS is in the `<style>` block. Key variables:

```css
:root {
    --bg-dark: #0a0a0a;
    --bg-panel: #1a1a1a;
    --orange: #ff8c00;
    --success: #00ff88;
    --error: #ff4444;
}
```

## Usage

### Quick Actions

- **Refresh All Data** - Manual data update (also auto-refreshes every 10s)
- **Trading Terminal** - Opens live trading terminal in new tab
- **View Logs** - (Coming soon) View bot execution logs
- **Emergency Stop** - (Coming soon) Kill all running bots

### Mobile

Fully responsive - single column layout on mobile with touch-friendly buttons.

## Future Enhancements

- [ ] Real-time data from OpenClaw APIs
- [ ] Parse trades.md for position data
- [ ] Historical P&L chart (7 days)
- [ ] Bot control (start/stop/restart)
- [ ] Log viewer modal
- [ ] Error log filtering
- [ ] WebSocket for live updates
- [ ] Email/Discord alerts on critical errors
- [ ] Export data (CSV/JSON)
- [ ] Custom refresh intervals

## Related Projects

- **Trading Terminal:** https://omarkanawati2000-netizen.github.io/omars-terminal/
- **OpenClaw Business:** https://omar-ai-agents.netlify.app
- **Landing Page Generator:** `ventures/landing_pages/mountain_view_roasters/`

## Demo for OpenClaw Business

This dashboard is perfect for showing potential clients:
- "Here's what managing your automation infrastructure looks like"
- Real-time visibility into all systems
- Professional, polished interface
- Shows the value of centralized monitoring

Include in pitches for **Professional** and **Enterprise** tier clients ($1,497+).
