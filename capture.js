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

  // Classic
  await page.goto(url);
  await page.evaluate(() => { localStorage.setItem('RR_DATA', JSON.stringify({preset:'classic'})); location.reload(); });
  await page.waitForNavigation();
  await capture('classic');

  // HD
  await page.evaluate(() => { localStorage.setItem('RR_DATA', JSON.stringify({preset:'hd'})); location.reload(); });
  await page.waitForNavigation();
  await capture('hd');

  // Deluxe
  await page.evaluate(() => { localStorage.setItem('RR_DATA', JSON.stringify({preset:'deluxe'})); location.reload(); });
  await page.waitForNavigation();
  await capture('deluxe');

  await browser.close();
})();
