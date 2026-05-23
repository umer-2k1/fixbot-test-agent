from browser_use import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = ChatGroq(
    model="llama3-70b-8192"
)

async def run():

    agent = Agent(
        task="""
        Go to google.com
        Search for OpenAI
        """,
        llm=llm
    )

    await agent.run()

asyncio.run(run())