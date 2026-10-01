// X4 independent evaluator. Arms run on copies of index.html only;
// this script is the grading oracle and is never part of an arm's tree.
// Usage: node assert.mjs <fixtureDir> [screenshotPath]
// Exit 0 iff ALL checks pass. Prints one JSON object.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

function chromiumSync() {
  const cache = path.join(process.env.HOME, '.npm/_npx');
  for (const d of fs.readdirSync(cache)) {
    const p = path.join(cache, d, 'node_modules/playwright-core');
    if (fs.existsSync(path.join(p, 'package.json'))) {
      const req = createRequire(path.join(p, 'package.json'));
      return req(p).chromium;
    }
  }
  throw new Error('playwright-core not found in npx cache');
}

const dir = process.argv[2];
const shot = process.argv[3];

const chromium = chromiumSync();
const browser = await chromium.launch({
  executablePath: '/opt/meta-chromium/chrome',
  args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.goto('file://' + path.resolve(dir, 'index.html'));

const checks = {};
// Check 1: click increments #count (two clicks -> "2").
await page.click('#add-btn');
await page.click('#add-btn');
const countText = (await page.textContent('#count')).trim();
checks.click_updates_count = countText === '2';

// Check 2: computed contrast of #status text vs effective background >= 4.5.
checks.contrast_ratio = await page.evaluate(() => {
  const el = document.getElementById('status');
  function rgb(s) {
    const m = s.match(/rgba?\(([^)]+)\)/);
    const parts = m[1].split(',').map(Number);
    return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
  }
  function bgOf(node) {
    while (node) {
      const c = rgb(getComputedStyle(node).backgroundColor);
      if (c.a > 0) return c;
      node = node.parentElement;
    }
    return { r: 255, g: 255, b: 255 };
  }
  function lum({ r, g, b }) {
    const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  }
  const fg = rgb(getComputedStyle(el).color);
  const bgc = bgOf(el);
  const l1 = lum(fg), l2 = lum(bgc);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
});
checks.contrast_aa = checks.contrast_ratio >= 4.5;

// Check 3: #add-btn carries a non-empty aria-label.
const aria = await page.getAttribute('#add-btn', 'aria-label');
checks.aria_label_present = !!(aria && aria.trim().length > 0);

if (shot) await page.screenshot({ path: shot });
await browser.close();

const pass = checks.click_updates_count && checks.contrast_aa && checks.aria_label_present;
console.log(JSON.stringify({ pass, countText, ariaLabel: aria, checks }));
process.exit(pass ? 0 : 1);
