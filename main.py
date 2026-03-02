from dotenv import load_dotenv
import os
import discord
from langchain.messages import HumanMessage


# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)
from agent import agent

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    async with message.channel.typing():
        content=message.content
        response=agent.invoke(
            {
                "messages":[HumanMessage(content)]
            }
        )
        agent_message=response["messages"][-1].text
    await message.channel.send(agent_message)

    
# Run bot with token
client.run(os.getenv("DISCORD_API_KEY"))