import asyncio
import requests
from telethon import TelegramClient

# --- CONFIGURATION ---
API_ID = 12345678                          # Get from my.telegram.org
API_HASH = 'your_api_hash_here'             # Get from my.telegram.org
SESSION_NAME = 'user_session'              # Local session name
CHAT_TARGET = 'Kryptosfera'                 # Target group title or username
N8N_WEBHOOK_URL = 'http://localhost:5678/webhook-test/fetch-telegram' # Your n8n Webhook Test URL

async def fetch_and_send():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        chat = await client.get_entity(CHAT_TARGET)
        cleaned_messages = []

        # Iterate over recent group messages
        async for msg in client.iter_messages(chat, limit=200):
            if not msg.text or not msg.date:
                continue

            # General topic messages in Telegram forums have no topic header or topic_id = 1
            reply_header = getattr(msg, 'reply_to', None)
            topic_id = getattr(reply_header, 'reply_to_top_id', None) or getattr(reply_header, 'reply_to_msg_id', None)
            
            if topic_id is None or topic_id == 1:
                sender = 'User'
                if msg.sender:
                    sender = getattr(msg.sender, 'username', None) or getattr(msg.sender, 'first_name', 'User')

                cleaned_messages.append({
                    'timestamp': int(msg.date.timestamp()),
                    'formattedDate': msg.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'person': f"@{sender}" if not sender.startswith('@') else sender,
                    'text': msg.text.strip()
                })

        # Sort chronologically (oldest to newest)
        cleaned_messages.sort(key=lambda x: x['timestamp'])

        # Format transcript block
        transcript = "\n".join([f"[{m['formattedDate']}] {m['person']}: {m['text']}" for m in cleaned_messages])

        payload = {
            'hasMessages': len(cleaned_messages) > 0,
            'transcript': transcript,
            'messageCount': len(cleaned_messages)
        }

        # Send extracted data to n8n Webhook
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        print("Data sent to n8n. Response status:", response.status_code)

if __name__ == '__main__':
    asyncio.run(fetch_and_send())