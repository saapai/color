"""
Slack Message History Fetcher - Skeletal Structure

Prerequisites:
1. Create a Slack App at https://api.slack.com/apps
2. Add OAuth Scopes:
   - channels:history (for public channels)
   - groups:history (for private channels)
   - im:history (for direct messages)
   - mpim:history (for group direct messages)
3. Install the app to your workspace
4. Get your OAuth Access Token from the OAuth & Permissions page
5. Get the Channel ID (right-click on channel > View channel details > bottom of popup)
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


class SlackHistoryFetcher:
    """Fetches message history from Slack workspace using the Slack API"""
    
    def __init__(self, token: str):
        """
        Initialize the Slack History Fetcher
        
        Args:
            token: Your Slack Bot User OAuth Token (starts with xoxb-)
                   or User OAuth Token (starts with xoxp-)
        """
        self.token = token
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def fetch_conversation_history(
        self, 
        channel_id: str, 
        limit: int = 100,
        oldest: Optional[str] = None,
        latest: Optional[str] = None,
        cursor: Optional[str] = None
    ) -> Dict:
        """
        Fetch conversation history from a Slack channel
        
        Args:
            channel_id: The ID of the channel (e.g., "C1234567890")
            limit: Number of messages to retrieve (max 1000, default 100)
            oldest: Only messages after this Unix timestamp (inclusive)
            latest: Only messages before this Unix timestamp (exclusive)
            cursor: Pagination cursor for fetching next page
        
        Returns:
            Dictionary containing messages and metadata
        """
        endpoint = f"{self.base_url}/conversations.history"
        
        # Build request parameters
        params = {
            "channel": channel_id,
            "limit": limit
        }
        
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        if cursor:
            params["cursor"] = cursor
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("ok"):
                print(f"Error: {data.get('error')}")
                return {}
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}
    
    def fetch_all_messages(
        self, 
        channel_id: str,
        oldest: Optional[str] = None,
        latest: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch all messages from a channel using pagination
        
        Args:
            channel_id: The ID of the channel
            oldest: Only messages after this Unix timestamp
            latest: Only messages before this Unix timestamp
        
        Returns:
            List of all messages
        """
        all_messages = []
        cursor = None
        
        while True:
            data = self.fetch_conversation_history(
                channel_id=channel_id,
                cursor=cursor,
                oldest=oldest,
                latest=latest,
                limit=200  # Max out for efficiency
            )
            
            if not data:
                break
            
            messages = data.get("messages", [])
            all_messages.extend(messages)
            
            # Check if there are more messages
            if not data.get("has_more", False):
                break
            
            # Get cursor for next page
            cursor = data.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
            
            print(f"Fetched {len(all_messages)} messages so far...")
        
        return all_messages
    
    def list_channels(self) -> List[Dict]:
        """
        List all channels in the workspace
        
        Returns:
            List of channel objects with id, name, and other metadata
        """
        endpoint = f"{self.base_url}/conversations.list"
        
        params = {
            "types": "public_channel,private_channel",  # Adjust as needed
            "limit": 200
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("ok"):
                return data.get("channels", [])
            else:
                print(f"Error: {data.get('error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
    
    def get_user_info(self, user_id: str) -> Dict:
        """
        Get information about a user
        
        Args:
            user_id: The Slack user ID
        
        Returns:
            Dictionary containing user information
        """
        endpoint = f"{self.base_url}/users.info"
        
        params = {"user": user_id}
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("ok"):
                return data.get("user", {})
            else:
                print(f"Error: {data.get('error')}")
                return {}
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}


def format_timestamp(ts: str) -> str:
    """Convert Slack timestamp to readable format"""
    timestamp = float(ts)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def main():
    """Example usage"""
    
    # TODO: Replace with your actual Slack token
    SLACK_TOKEN = "xoxb-your-token-here"
    
    # TODO: Replace with your channel ID
    CHANNEL_ID = "C1234567890"
    
    # Initialize the fetcher
    fetcher = SlackHistoryFetcher(SLACK_TOKEN)
    
    # Example 1: List all channels
    print("Fetching channels...")
    channels = fetcher.list_channels()
    for channel in channels:
        print(f"Channel: {channel['name']} (ID: {channel['id']})")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Fetch recent messages from a channel
    print(f"Fetching messages from channel {CHANNEL_ID}...")
    data = fetcher.fetch_conversation_history(
        channel_id=CHANNEL_ID,
        limit=10  # Get last 10 messages
    )
    
    if data and data.get("messages"):
        for message in data["messages"]:
            timestamp = format_timestamp(message["ts"])
            text = message.get("text", "")
            user = message.get("user", "Unknown")
            print(f"[{timestamp}] {user}: {text}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Fetch all messages from a specific date range
    # Convert dates to Unix timestamps
    # oldest_ts = "1634000000"  # October 12, 2021
    # latest_ts = "1634086400"  # October 13, 2021
    
    # all_messages = fetcher.fetch_all_messages(
    #     channel_id=CHANNEL_ID,
    #     oldest=oldest_ts,
    #     latest=latest_ts
    # )
    
    # print(f"Total messages fetched: {len(all_messages)}")
    
    # Example 4: Save messages to JSON file
    # with open("slack_messages.json", "w") as f:
    #     json.dump(all_messages, f, indent=2)
    # print("Messages saved to slack_messages.json")


if __name__ == "__main__":
    main()

