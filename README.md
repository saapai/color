# Slack Message History Fetcher

A Python skeleton for fetching message history from your Slack workspace using the Slack API.

## Setup Instructions

### 1. Create a Slack App
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name your app and select your workspace

### 2. Configure OAuth Scopes
1. Go to "OAuth & Permissions" in the left sidebar
2. Scroll to "Scopes" → "Bot Token Scopes"
3. Add these scopes:
   - `channels:history` - View messages in public channels
   - `channels:read` - View basic channel info
   - `groups:history` - View messages in private channels
   - `groups:read` - View basic private channel info
   - `im:history` - View messages in direct messages
   - `mpim:history` - View messages in group DMs
   - `users:read` - View user information

### 3. Install App to Workspace
1. Scroll to top of "OAuth & Permissions" page
2. Click "Install to Workspace"
3. Authorize the app
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### 4. Get Channel ID
- Right-click on any channel → "View channel details"
- Scroll to bottom of popup to see Channel ID (e.g., `C1234567890`)

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Update the Code
Open `slack_history_fetcher.py` and replace:
- `SLACK_TOKEN` with your OAuth token
- `CHANNEL_ID` with your channel ID

### 7. Run
```bash
python slack_history_fetcher.py
```

## Features

- ✅ Fetch conversation history from any channel
- ✅ Automatic pagination to get all messages
- ✅ List all channels in workspace
- ✅ Get user information
- ✅ Date range filtering
- ✅ Export messages to JSON

## API Rate Limits

Slack has rate limits (Tier 3: 50+ requests per minute). The script handles pagination appropriately.