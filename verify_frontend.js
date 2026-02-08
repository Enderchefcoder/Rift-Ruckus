const puppeteer = require('puppeteer');
const path = require('path');

async function run() {
    const args = process.argv.slice(2);
    const filename = args[0] || 'screenshot.png';
    const x = parseFloat(args[1]) || 0;
    const y = parseFloat(args[2]) || 0;
    const z = parseFloat(args[3]) || 0;

    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });

    const filePath = 'file://' + path.join(__dirname, 'index.html');
    await page.goto(filePath);

    // Wait for loader to disappear
    await page.waitForFunction(() => {
        const ld = document.getElementById('LD');
        return ld && ld.classList.contains('gone');
    }, { timeout: 10000 });

    // Teleport player
    await page.evaluate((x, y, z) => {
        if (window.player) {
            window.player.position.set(x, y, z);
        }
    }, x, y, z);

    // Wait for a few frames
    await new Promise(r => setTimeout(r, 2000));

    await page.screenshot({ path: filename });
    console.log('Saved ' + filename);
    await browser.close();
}

run().catch(err => {
    console.error(err);
    process.exit(1);
});
