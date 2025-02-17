from langchain_openai import ChatOpenAI
from browser_use import Agent
import env

import asyncio

llm = ChatOpenAI(model="gpt-4o", api_key=env.OPENAI_KEY)

async def main():
    agent = Agent(
        task="Based on the NDX chart for the last 2 weeks, what would be the NDX price range on Feb 18?",
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())

# Result: Based on the recent NDX data, the estimated price range for February 18, 2025, is between 21,700 and 22,150.
