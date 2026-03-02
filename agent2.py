from dotenv import load_dotenv
import os
import discord
import asyncio
import base64
import io

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langchain_openai import ChatOpenAI

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
def generateAndSendImage(prompt:str):
    """Use this tool to generate image from prompt and send it to user"""
    llm = ChatOpenAI(model="gpt-4.1-mini")

    config=runTime.config.get("configurable")
    message=config.get("message")
    config.get("loop")


    tool = {"type": "image_generation", "quality": "low"}
    llm_with_tools = llm.bind_tools([tool])

    ai_message = llm_with_tools.invoke(
        {
            "messages":[HumanMessage(prompt)]
        }
    )
    #String to image conversion
    image=ai_message.content_blocks[0]["base64"]

    base64_string=base64.b64decode(image)
    image_bytes=io.BytesIO(base64_string)
    file=discord.File(fp=image_bytes,filename="image.png")
    asyncio.run_coroutine_threadsafe(message.channel.send(file=file),loop)
    return "Image generated and send successfully"

    
@tool
def surfInternet(query:str):
    """Use this tool to surf the internet and get latest information"""
    result=tavily_client.search(query=query)
    print(result)
    return str(result)

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# agent=create_agent(model=model,tools=[surfInternet,generateAndSendImage],system_prompt="""Provide clean out to the user""")
agent=create_agent(model=model,tools=[surfInternet],system_prompt="""Provide clean out to the user""")


