const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 800, height: 600 } });

  const url = 'file://' + path.resolve('index.html');

  const capture = async (name, action) => {
    await page.goto(url);
    await page.waitForSelector('#LD.gone', { timeout: 20000 });
    if(action) await page.evaluate(action);
    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'gameplay/' + name + '.png' });
    console.log('Captured ' + name);
  };

  // Main Lobby with new HUD
  await capture('new_lobby_hud');

  // Character Select
  await capture('new_char_select', () => show('oChar'));

  // Settings
  await capture('new_settings', () => show('oSettings'));

  // Modes
  await capture('new_modes', () => { show('oPortal'); loadModes(); });

  // Results
  await capture('new_results', () => {
    // Mock scores
    P.score = 1250;
    showResults();
  });

  await browser.close();
})();
