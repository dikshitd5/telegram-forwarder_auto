# Import necessary modules
from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession
import os

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

# BLOCKED_TEXTS = config("BLOCKED_TEXTS", default="", cast=lambda x: [i.strip().lower() for i in x.split(',')])
# MEDIA_FORWARD_RESPONSE = config("MEDIA_FORWARD_RESPONSE", default="yes").lower()

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

# Initialize another bot client
bot = TelegramClient("bot_session", api_id=APP_ID, api_hash=API_HASH)

# Event handler for incoming messages
@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            message_text = event.raw_text.lower()

            # if any(blocked_text in message_text for blocked_text in BLOCKED_TEXTS):
            #     print(f"Blocked message containing one of the specified texts: {event.raw_text}")
            #     logging.warning(f"Blocked message containing one of the specified texts: {event.raw_text}")
            #     continue

            # if event.media:
            #     user_response = MEDIA_FORWARD_RESPONSE
            #     if user_response != 'yes':
            #         print(f"Media forwarding skipped by user for message: {event.raw_text}")
            #         continue

                # Forward media message to another bot
                await bot.forward_messages(i, event.message)

                print(f"Forwarded media message to bot {i}")

            else:
                # Forward text message to another bot
                await bot.send_message(i, event.raw_text)
                print(f"Forwarded text message to bot {i}")

        except Exception as e:
            print(f"Error forwarding message to bot {i}: {e}")

# Run the bot
print("Bot has started.")
steallootdealUser.run_until_disconnected()
