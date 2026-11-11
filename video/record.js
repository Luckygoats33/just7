// Records video/explainer.html to a 1920x1080 webm in real time (about 60s).
const { chromium } = require('playwright');
const path = require('path');
const { pathToFileURL } = require('url');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const ctx = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: path.join(__dirname, 'raw'), size: { width: 1920, height: 1080 } },
  });
  const page = await ctx.newPage();
  await page.goto(pathToFileURL(path.join(__dirname, 'explainer.html')).href);
  await page.waitForTimeout(61000);
  const v = page.video();
  await ctx.close();
  await browser.close();
  console.log(await v.path());
})();
