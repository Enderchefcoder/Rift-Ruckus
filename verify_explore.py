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
        await page.click('#social-btn')
        await asyncio.sleep(1)
        # Click the Explore tab (it's the second button in socialTabs)
        await page.click('#socialTabs button:nth-child(2)')
        await asyncio.sleep(1)
        await page.screenshot(path='/home/jules/verification/social_explore_mobile.png')
        print("Social explore mobile screenshot saved.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
