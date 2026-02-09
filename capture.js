const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });

  const url = 'file://' + path.resolve('index.html');

  const capture = async (name, setupFn) => {
    await page.goto(url);
    if(setupFn) await page.evaluate(setupFn);
    await page.waitForSelector('#LD.gone', { timeout: 15000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: 'gameplay/' + name + '.png' });
    console.log('Captured ' + name);
  };

  // Deluxe HD (already verified but good to keep)
  await capture('deluxe', () => { localStorage.setItem('RR_DATA', JSON.stringify({preset:'deluxe'})); });

  // Halloween
  await capture('halloween', () => {
    localStorage.setItem('RR_DATA', JSON.stringify({preset:'hd'}));
    // Mock date to October
    window.Date = class extends Date {
      constructor() { super('2024-10-31'); }
    };
  });

  // Spring
  await capture('spring', () => {
    window.Date = class extends Date {
      constructor() { super('2024-04-15'); }
    };
  });

  // Social Menu
  await capture('social_menu', async () => {
     // Mock some friends
     localStorage.setItem('RR_DATA', JSON.stringify({friends: ['Zippy', 'Sparky'], invited: ['Zippy']}));
  });
  // Open social menu
  await page.evaluate(() => { show('oSocial'); loadSocial(); });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'gameplay/social_menu.png' });

  await browser.close();
})();
