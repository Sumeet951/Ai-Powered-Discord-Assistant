from dotenv import load_dotenv
import os
import discord

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send('Hello from the bot!')
# Run bot with token
client.run(os.getenv("DISCORD_API_KEY"))