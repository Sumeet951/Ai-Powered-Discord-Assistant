from dotenv import load_dotenv
import os
import discord
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient
load_dotenv()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool
def surfInternet(query:str):
    """Use this tool to surf the internet and get latest information"""
    result=tavily_client.search(query=query)
    return str(result)



model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
agent=create_agent(model=model,tools=[surfInternet],system_prompt="""Provide clean out to the user""")
