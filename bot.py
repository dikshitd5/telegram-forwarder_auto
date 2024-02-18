# Import necessary modules
from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession
import os
import asyncio

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Print starting message
print("Starting...")

# Read configuration from environment variables
APP_ID = config("APP_ID", default=0, cast=int)
API_HASH = config("API_HASH", default=None, cast=str)
SESSION = config("SESSION", default="", cast=str)
FROM_ = config("FROM_CHANNEL", default="", cast=str)
TO_ = config("TO_CHANNEL", default="", cast=str)

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

YOUR_ADMIN_USER_ID = config("YOUR_ADMIN_USER_ID", default=0, cast=int)
BOT_API_KEY = config("BOT_API_KEY", default="", cast=str)

# Initialize Telethon client
try:
    steallootdealUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    steallootdealUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Define a queue for messages
message_queue = []

# Function to handle message forwarding
async def forward_messages():
    while True:
        if message_queue:
            message = message_queue.pop(0)
            for i in TO:
                try:
                    if message.media:
                        await steallootdealUser.send_message(i, message.text, file=message.media)
                        print(f"Forwarded media message to channel {i}")
                    else:
                        await steallootdealUser.send_message(i, message.text)
                        print(f"Forwarded text message to channel {i}")
                except Exception as e:
                    print(f"Error forwarding message to channel {i}: {e}")
        await asyncio.sleep(60)  # Wait for 1 minute before checking the queue again

# Event handler for incoming messages
@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM))
async def queue_messages(event):
    message_queue.append(event.message)

# Run the bot
print("Bot has started.")
asyncio.ensure_future(forward_messages())
steallootdealUser.run_until_disconnected()
