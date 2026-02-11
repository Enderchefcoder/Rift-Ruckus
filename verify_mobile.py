import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Set viewport to a common mobile size (portrait)
        context = await browser.new_context(
            viewport={'width': 375, 'height': 667},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/004.1'
        )
        page = await context.new_page()

        # Load the local index.html
        file_path = "file://" + os.path.abspath("index.html")
        await page.goto(file_path)

        # Wait for loading screen to finish
        await asyncio.sleep(5)

        # Take a screenshot of the lobby
        await page.screenshot(path='/home/jules/verification/gameplay_lobby_mobile.png')
        print("Lobby mobile screenshot saved.")

        # Open Social Menu
        await page.click('#social-btn')
        await asyncio.sleep(1)
        await page.screenshot(path='/home/jules/verification/social_mobile.png')
        print("Social menu mobile screenshot saved.")

        # Close Social and start a game (using debug)
        await page.evaluate("window.hide('oSocial')")
        await page.evaluate("window.startMinigame({id:'sumo', name:'SUMO RING', tip:'TEST', dur:30, type:'sumo'})")
        await asyncio.sleep(5) # Wait for countdown
        await page.screenshot(path='/home/jules/verification/gameplay_mobile.png')
        print("Gameplay mobile screenshot saved.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
