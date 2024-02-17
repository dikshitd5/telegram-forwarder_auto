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
TO = config("TO_CHANNEL", default="", cast=str)
BOT_USER_ID = config("BOT_USER_ID", default=0, cast=int)

YOUR_ADMIN_USER_ID = config("YOUR_ADMIN_USER_ID", default=0, cast=int)
BOT_API_KEY = config("BOT_API_KEY", default="", cast=str)

# Initialize Telethon client
try:
    steallootdealUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    steallootdealUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Event handler for incoming messages
@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            message_text = event.raw_text.lower()

            if event.media:
                user_response = MEDIA_FORWARD_RESPONSE
                if user_response != 'yes':
                    print(f"Media forwarding skipped by user for message: {event.raw_text}")
                    continue

                await steallootdealUser.send_message(i, message_text, file=event.media)
                print(f"Forwarded media message to channel {i}")

            else:
                await steallootdealUser.send_message(i, message_text)
                print(f"Forwarded text message to channel {i}")

        except Exception as e:
            print(f"Error forwarding message to channel {i}: {e}")
    
    # Forward the message to specified users
    for user_id in USERS_TO_FORWARD:
        try:
            await steallootdealUser.send_message(user_id, event.raw_text)
            print(f"Forwarded message to user {user_id}")
        except Exception as e:
            print(f"Error forwarding message to user {user_id}: {e}")

# Event handler for incoming messages
@client.on(events.NewMessage(chats=CHANNEL_TO_MONITOR))
async def forward_to_bot(event):
    try:
        await client.forward_messages(BOT_USER_ID, event.message)
        print("Message forwarded to bot.")
    except Exception as e:
        print(f"Error forwarding message to bot: {e}")

# Run the bot
print("Bot has started.")
steallootdealUser.run_until_disconnected()
