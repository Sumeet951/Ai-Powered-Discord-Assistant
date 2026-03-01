from dotenv import load_dotenv
import os
import discord
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create client
client = discord.Client(intents=intents)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def surfInternet(query:str):
    """Use this tool to surf the internet and get latest information"""
    result=tavily_client.search(query=query)
    print(result)
    return str(result)



model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

agent=create_agent(model=model,tools=[surfInternet],system_prompt="""Provide clean out to the user""")
@client.event
async def on_message(message):
    if message.author == client.user:
        return
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