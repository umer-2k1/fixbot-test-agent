from typing import Any
import asyncio
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent, Browser, ChatGroq, Tools

DEFAULT_TASK = """
    Design me a mid-range water-cooled ITX computer
    Keep the total budget under $2000

    Go to https://pcpartpicker.com/
    Make sure the build is complete and has no incompatibilities.
    Provide the full list of parts with prices and a link to the completed build.
    """


def _headless() -> bool:
	raw = os.getenv("BROWSER_USE_HEADLESS", "true").lower()
	return raw in ("1", "true", "yes", "on")


def _groq_model() -> str:
	model = os.getenv("GROQ_MODEL", "meta-llama/llama-4-maverick-17b-128e-instruct").strip()
	if not model:
		print("GROQ_MODEL is empty. Set it in .env or remove it to use default.", file=sys.stderr)
		sys.exit(1)
	return model


async def main():
	# Browser-Use launches Chromium locally (no CDP / external Chrome required)
	browser = Browser(headless=_headless())

	llm = ChatGroq(
		model=_groq_model(),
		api_key=os.environ.get("GROQ_API_KEY"),
	)

	tools = Tools[Any]()

	task = os.getenv("AGENT_TASK", DEFAULT_TASK).strip()

	agent = Agent[Any, Any](
		task=task,
		browser=browser,
		tools=tools,
		llm=llm,
	)

	max_steps = int(os.getenv("AGENT_MAX_STEPS", "100000"))
	history = await agent.run(max_steps=max_steps)
	return history


if __name__ == "__main__":
	history = asyncio.run(main())
	final_result = history.final_result()
	print(final_result)
