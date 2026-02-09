const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });

  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));

  const url = 'file://' + path.resolve('index.html');

  console.log('Capturing screenshots...');

  const capture = async (name) => {
    try {
      await page.waitForSelector('#hud', { state: 'visible', timeout: 15000 });
      await page.waitForTimeout(3000); // Give it time to render
      await page.screenshot({ path: 'gameplay/' + name + '.png' });
      console.log('Captured ' + name);
    } catch(e) {
      console.log('Failed to capture ' + name + ': ' + e.message);
      await page.screenshot({ path: 'gameplay/error_' + name + '.png' });
    }
  };

  const presets = ['classic', 'hd', 'deluxe'];

  await page.goto(url);

  for (const preset of presets) {
    await page.evaluate((p) => {
      const data = JSON.parse(localStorage.getItem('RR_DATA') || '{}');
      data.preset = p;
      localStorage.setItem('RR_DATA', JSON.stringify(data));
      location.reload();
    }, preset);
    await page.waitForNavigation();
    await capture(preset);
  }

  await browser.close();
})();
