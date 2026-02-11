import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 375, 'height': 667})
        page = await context.new_page()
        file_path = "file://" + os.path.abspath("index.html")
        await page.goto(file_path)
        await asyncio.sleep(5)
        await page.click('#hud > div:first-child') # Click the player card to open avatar selection
        await asyncio.sleep(1)
        await page.screenshot(path='/home/jules/verification/avatars_mobile.png')
        print("Avatars mobile screenshot saved.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
