import os
import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 720})

        # Listen for console messages
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))

        url = f'file://{os.getcwd()}/index.html'
        print(f"Loading {url}")
        page.goto(url)

        # Wait for game to init
        time.sleep(5)

        def take_screenshot(name, x, y, z):
            print(f"Teleporting to {name} at ({x}, {y}, {z})")
            page.evaluate(f"() => {{ if(window.player) {{ window.player.position.set({x}, {y}, {z}); console.log('Teleported ' + '{name}'); }} else {{ console.error('player not found'); }} }}")
            time.sleep(2)
            page.screenshot(path=f'/home/jules/verification/final_{name}.png')

        # Lobby
        page.screenshot(path='/home/jules/verification/final_lobby_v3.png')

        # Teleport to different games
        take_screenshot('sumo_v3', 0, 5, -50)
        take_screenshot('hill_v3', 50, 5, -50)
        take_screenshot('pads_v3', -50, 5, -50)
        take_screenshot('tag_v3', 50, 5, 50)
        take_screenshot('stars_v3', -50, 5, 50)

        browser.close()

if __name__ == "__main__":
    run()
