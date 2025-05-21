from browser_use import Controller, ActionResult, Browser, BrowserConfig
from browser_use import Agent
from langchain_together import ChatTogether
import asyncio
from dotenv import load_dotenv

load_dotenv()

url = "https://job-boards.greenhouse.io/contentful/jobs/6776532?gh_jid=6776532#app"

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        browser_binary_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        extra_browser_args=[
            "--user-data-dir=/Users/yo/Library/Application Support/Google/Chrome/Default",
        ]
    )
)

controller = Controller()
llm = ChatTogether(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
)

@controller.action('Open website')
async def open_website(url: str, browser: Browser):
    page = await browser.get_current_page()
    await page.goto(url)
    return ActionResult(extracted_content='Website opened')

async def main():
    # Create the agent with your configured browser
    agent = Agent(
        task=f"Given a job application url: {url}, open the url in the browser and find and read all input field names and types and return them as a list of strings.",
        llm=llm,
        browser=browser,
        controller=controller,
    )
    
    result = await agent.run()
    print('----RESULT----')
    print(result.final_result())
    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
