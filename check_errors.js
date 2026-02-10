const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => { console.log('PAGE LOG:', msg.text()); });
  page.on('pageerror', err => { console.log('PAGE ERROR:', err.message); });

  const url = 'file://' + path.resolve('index.html');
  await page.goto(url);

  // Wait for the .gone class to be added
  try {
    await page.waitForSelector('#LD.gone', { state: 'attached', timeout: 15000 });
    console.log('Class .gone attached.');
  } catch(e) {
    console.log('Class .gone NOT attached: ' + e.message);
  }

  await browser.close();
})();
