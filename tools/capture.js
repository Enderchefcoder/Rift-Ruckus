const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });

  const url = 'file://' + path.resolve('index.html');

  const capture = async (name, action) => {
    try {
      fs.mkdirSync('gameplay', { recursive: true });
      await page.goto(url);
      await page.waitForSelector('#LD.gone', { state: 'attached', timeout: 20000 });
      if(action) await page.evaluate(action);
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'gameplay/' + name + '.png' });
      console.log('Captured ' + name);
    } catch(e) {
      console.log('Error capturing ' + name + ': ' + e.message);
    }
  };

  await capture('new_lobby_hud');
  await capture('new_char_select', () => { window.show('oChar'); window.loadChars(); });
  await capture('new_settings', () => window.show('oSettings'));
  await capture('new_modes', () => window.loadModes() || window.show('oPortal'));
  await capture('new_results', () => {
    P.score = 1250;
    showResults();
  });

  await browser.close();
})();
