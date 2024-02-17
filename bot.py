#    Copyright (c) 2021 Ayush
#    
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.
# 
#    License can be found in < https://github.com/Ayush7445/telegram-auto_forwarder/blob/main/License > .

# Import necessary modules
# Import necessary modules
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
FROM_CHANNEL = config("FROM_CHANNEL", default="", cast=str)
TO_BOT = config("TO_BOT", default="", cast=str)
YOUR_ADMIN_USER_ID = config("YOUR_ADMIN_USER_ID", default=0, cast=int)

# Initialize Telethon client
try:
    client = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    client.start()
except Exception as e:
    print(f"ERROR - {e}")
    exit(1)

# Event handler for incoming messages
@client.on(events.NewMessage(chats=FROM_CHANNEL))
async def forward_to_bot(event):
    try:
        # Forward the message to the target bot
        await client.forward_messages(TO_BOT, event.message)
        print(f"Forwarded message to bot {TO_BOT}")
    except Exception as e:
        print(f"Error forwarding message to bot {TO_BOT}: {e}")

# Run the client
print("Bot has started.")
client.run_until_disconnected()

