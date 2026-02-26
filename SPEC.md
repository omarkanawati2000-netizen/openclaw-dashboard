# OpenClaw Dashboard Specification

## Overview
Build a comprehensive monitoring and control dashboard for Omar's OpenClaw automation infrastructure.

## Design Style
- **Dark theme** similar to the trading terminal (Bloomberg-inspired)
- **Orange/amber accents** on black background
- **IBM Plex Mono** or similar monospace font
- **Responsive** - works on desktop and mobile
- **Single HTML file** with inline CSS/JS (no external dependencies except fonts)

## Core Sections

### 1. 🤖 Bot Status Panel
Display all active cron jobs and their health:
- **Cron jobs to track:**
  - RSI Bot (every 30 min)
  - SMC Bot (every hour)
  - Arc Highlightz Clip Engine (every 30 min)
  - FomoHighlights Clip Engine (every 30 min at :15/:45)
  - Content Bot Health Monitor (hourly)
  - Data Collector (periodic)
  - Morning Market Briefing (daily)
  - Idea Generator (periodic)
  - Daily Security Scan (daily)

**For each bot show:**
- Name
- Status (Running / Idle / Error)
- Last run timestamp
- Next run time
- Success/error count (last 24h)
- Quick action button (View Logs / Restart)

**Data source:** Mock data initially, with placeholders for real API integration

### 2. 📈 Trading Dashboard
Real-time trading performance metrics:

**Current Positions:**
- Coin name, direction (LONG/SHORT), size, entry price
- Current P&L ($ and %)
- Stop loss / Take profit levels
- Data source: Read from `../../../memory/trades.md` (parse the OPEN positions)

**Daily Statistics:**
- Total P&L today
- Win rate (%)
- Active positions count
- Best performer (biggest gain)
- Worst performer (biggest loss)

**Performance Chart:**
- Line chart showing cumulative P&L over last 7 days
- Mock data initially

### 3. 🎬 Content Engine Stats
YouTube channel performance:

**Arc Highlightz:**
- Clips uploaded today / this week
- Total views (last 7 days)
- Subscriber count
- Latest clip info

**FomoHighlights:**
- Same metrics as Arc Highlightz

**Upload Queue:**
- Pending uploads count
- Last successful upload timestamp
- YouTube API quota remaining (out of 10,000 daily)

**Data source:** Mock data initially

### 4. 💰 Revenue Tracker
Track income streams and goals:

**Active Revenue Streams:**
- OpenClaw business (current MRR, new clients this month)
- Trading (monthly P&L)
- Content monetization (ad revenue estimate)
- Solana Sentiment Hunter (subscribers)

**Goals Progress:**
- Monthly revenue target with progress bar
- Year revenue target
- Milestones (1K subs, $10K/mo, etc.)

**Data source:** Mock data with manual update capability

### 5. ⚙️ System Health
Infrastructure monitoring:

**API Quotas:**
- OpenAI API usage (% of limit)
- YouTube API quota (units used / 10,000)
- Hyperliquid API rate limit status
- Twitch API calls remaining

**Disk Space:**
- Workspace size
- Clip storage used
- Data folder size

**Recent Errors:**
- Last 5 errors across all systems
- Timestamp, source, error message
- Clear button

**Data source:** Mock data initially

### 6. 🎯 Quick Actions Bar (Top)
Buttons for common tasks:
- Refresh All Data
- Open Trading Terminal
- View Logs
- Emergency Stop (kills all bots)
- Open Workspace
- Settings

## Technical Requirements

### File Structure
```
openclaw_dashboard/
├── index.html (single-file app with inline CSS/JS)
├── SPEC.md (this file)
└── README.md (deployment instructions)
```

### Data Integration
**Phase 1 (MVP):** Mock data for all sections - get the UI working first

**Phase 2 (Future):** Real integrations
- Read trades.md for positions
- Parse OpenClaw cron status
- Query Hyperliquid API
- Query YouTube API
- Read log files

### Update Mechanism
- Auto-refresh every 10 seconds
- Manual refresh button
- Visual indicator when data is loading

### Responsive Design
- Desktop: Multi-column grid layout
- Mobile: Single column, collapsible sections
- Touch-friendly buttons on mobile

### Performance
- Fast initial load (<2s)
- Smooth animations (CSS transitions)
- No heavy frameworks (vanilla JS)

## Deployment
- Deploy to GitHub Pages like the trading terminal
- URL: `https://omarkanawati2000-netizen.github.io/openclaw-dashboard/`
- Include deployment script

## Success Criteria
✅ All 6 sections render correctly
✅ Dark theme with orange accents matches trading terminal aesthetic
✅ Responsive on desktop and mobile
✅ Mock data populates all sections
✅ Auto-refresh works
✅ Deployed and accessible via URL

## Reference
See trading terminal for style inspiration:
https://omarkanawati2000-netizen.github.io/omars-terminal/

## Timeline
Complete within 2-3 hours of agent time.

## Completion Notification
When finished, run:
```bash
openclaw system event --text "Done: OpenClaw Dashboard built and deployed" --mode now
```
