from playwright.async_api import async_playwright
import os

async def run_scenario(context, name, action=None):
    page = await context.new_page()
    file_path = "file://" + os.path.abspath("index.html")
    await page.goto(file_path)

    await page.wait_for_selector('#LD.gone', state='attached', timeout=20000)

    if action:
        await action(page)

    path = f"screenshots/{name}.png"
    await page.screenshot(path=path)
    print(f"Screenshot saved: {path}")
    await page.close()

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 375, 'height': 667})

        # Lobby
        await run_scenario(context, "mobile_lobby")

        # Social
        async def open_social(page):
            await page.click('#social-btn')
            await page.wait_for_selector('#oSocial.show')
        await run_scenario(context, "mobile_social", open_social)

        # Explore
        async def open_explore(page):
            await page.click('#social-btn')
            await page.wait_for_selector('#oSocial.show')
            await page.click('#socialTabs button:nth-child(2)')
            await page.wait_for_selector('#exItems')
        await run_scenario(context, "mobile_explore", open_explore)

        # Avatars
        async def open_avatars(page):
            await page.click('#hud > div:first-child')
            await page.wait_for_selector('#oChar.show')
        await run_scenario(context, "mobile_avatars", open_avatars)

        await browser.close()

if __name__ == "__main__":
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    import asyncio
    asyncio.run(verify())
