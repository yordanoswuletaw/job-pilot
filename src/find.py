from argparse import Action
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_together import ChatTogether
from pydantic import BaseModel, SecretStr

from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult


# Validate required environment variables
load_dotenv()
required_env_vars = ['TOGETHER_API_KEY', 'TAVILY_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

# Configure the browser to use Playwright's Chromium
# browser = Browser(
#     config=BrowserConfig(
#         browser_type="chrome",
#         browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
#         debug_port=9222,
#         headless=False, 
# 		disable_security=True,
#     )
# )

browser = Browser(
    config=BrowserConfig(
        browser_type="chromium",  # Uses Playwright’s Chromium
        headless=False,
		disable_security=True,
    )
)

controller = Controller()

# def list_famous_job_search_site() -> list[str]:
# 	return [
# 		'https://careers.google.com/jobs',
# 		'https://www.linkedin.com/jobs',
# 		'https://research.google/careers',
# 		'https://deepmind.google/about/careers',
# 		'https://www.amazon.jobs/en/jobs',
# 		'https://www.microsoft.com/en-us/jobs',
# 		'https://www.apple.com/jobs',
# 	]

@controller.action("open website")
async def open_website(url: str,  browser: Browser) -> ActionResult:
	page = await browser.get_current_page()
	await page.goto(url)
	return ActionResult(extracted_content='Website opened')

async def main():
	ground_task = '''You are a professional job finder.
	Your goal is to find job opportunities for junior AI engineers.
	Search relevant job opportunities for junior AI engineers.
	Return a list of the job title, job description url, and job application url as a json format.'''
	
	model = ChatTogether(
		model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
	)

	# Create the agent with your configured browser
	agent = Agent(
		task=ground_task,
		llm=model,
		browser=browser,
		controller=controller,
	)

	res = await agent.run()
	print(res)

	print(f"\nJob search completed! {res}")
	input('Press Enter to close the browser...')
	await browser.close()

if __name__ == '__main__':
	asyncio.run(main())