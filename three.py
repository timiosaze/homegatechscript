
import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
import os


async def main():
    # Launch the browser
    browser = await launch({"headless": True})

    # Open a new browser page
    page = await browser.newPage()

    # Create a URI for our test file
    page_path = "https://www.homegate.ch/rent/3002047552"

    # Open our test file in the opened page
    await page.goto(page_path,{
    'timeout': 1000*60 #The timeout here is 60s
	})
    page_content = await page.content()
    # element = await page.xpath('//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]/div[3]/section[1]/div[4]/dl/dd[5]')
    # title = await page.evaluate('(element) => element.textContent', element)
    
    print(page_content)

    # Close browser
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
