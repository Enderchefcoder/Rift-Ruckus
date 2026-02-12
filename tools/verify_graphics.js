const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 844, height: 390 }, // iPhone 12 Pro landscape
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
  });

  const url = 'file://' + path.resolve('index.html');
  await page.goto(url);
  await page.waitForTimeout(2000); // Wait for load

  // Helper to change preset and reload
  async function setMode(mode) {
    await page.evaluate((m) => {
      setPreset(m);
    }, mode);
    await page.waitForTimeout(3000); // Wait for reload and Three.js init
  }

  // Classic
  await setMode('classic');
  await page.screenshot({ path: 'lobby_classic.png' });
  console.log('Captured lobby_classic.png');

  // HD
  await setMode('hd');
  await page.screenshot({ path: 'lobby_hd.png' });
  console.log('Captured lobby_hd.png');

  // Deluxe
  await setMode('deluxe');
  await page.screenshot({ path: 'lobby_deluxe.png' });
  console.log('Captured lobby_deluxe.png');

  await browser.close();
})();
