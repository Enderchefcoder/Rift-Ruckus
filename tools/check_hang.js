const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  let errors = [];
  let failed = false;
  page.on('console', msg => {
    console.log('PAGE LOG:', msg.text());
    if (msg.type() === 'error') { errors.push(msg.text()); failed = true; }
  });
  page.on('pageerror', err => {
    console.log('CRITICAL ERROR:', err.message);
    errors.push(err.message);
    failed = true;
  });

  const url = 'file://' + path.resolve('index.html');
  console.log('Loading page...');
  await page.goto(url);

  // Wait for loading bar to reach 100%
  // The fill width is set in startLoad
  try {
    await page.waitForFunction(() => {
        const fill = document.getElementById('ldFill');
        return fill && fill.style.width === '100%';
    }, { timeout: 10000 });
    console.log('Loading bar reached 100%.');
  } catch(e) {
    failed = true;
    console.log('Loading bar did not reach 100%: ' + e.message);
  }

  // Wait a bit more to see if it transitions
  await page.waitForTimeout(2000);

  const isLobbyVisible = await page.evaluate(() => {
    const ld = document.getElementById('LD');
    return ld && ld.classList.contains('gone');
  });

  if (isLobbyVisible) {
    console.log('Successfully transitioned to lobby.');
  } else {
    failed = true;
    console.log('STUCK ON LOADING SCREEN.');
  }

  if (errors.length > 0) {
    failed = true;
    console.log('Found ' + errors.length + ' errors.');
  } else {
    console.log('No errors found!');
  }

  if (failed) process.exitCode = 1;

  await browser.close();
})();
