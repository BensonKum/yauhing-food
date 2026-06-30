const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });
  
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push('CONSOLE: ' + msg.text()); });
  page.on('pageerror', err => errors.push('PAGEERROR: ' + err.message));
  
  await page.goto('file:///C:/Users/user/.qclaw/workspace/yauhing-food/index.html', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 2500));
  
  // 1. Initial state: how many cards are hid vs not?
  const initial = await page.evaluate(() => {
    const all = document.querySelectorAll('.p-card');
    const hid = document.querySelectorAll('.p-card.hid');
    const visible = document.querySelectorAll('.p-card:not(.hid)');
    const activeCat = document.querySelector('.ct .t-btn.active')?.dataset?.cat;
    const activeFilter = document.querySelector('.f-btn.active')?.dataset?.filter;
    return {
      totalCards: all.length,
      hidCount: hid.length,
      visibleCount: visible.length,
      activeCat: activeCat,
      activeFilter: activeFilter,
      rcText: document.getElementById('rc')?.textContent
    };
  });
  
  // 2. Click 全部 category and dump
  await page.click('.ct .t-btn[data-cat="全部"]');
  await new Promise(r => setTimeout(r, 500));
  
  const afterClickAll = await page.evaluate(() => {
    const all = document.querySelectorAll('.p-card');
    const hid = document.querySelectorAll('.p-card.hid');
    const visible = Array.from(document.querySelectorAll('.p-card:not(.hid)'));
    // Find 醬油套裝 card now
    const target = Array.from(document.querySelectorAll('.p-card')).find(
      c => c.querySelector('.p-name')?.textContent.trim() === '醬油套裝'
    );
    return {
      totalCards: all.length,
      hidCount: hid.length,
      visibleCount: visible.length,
      targetExists: !!target,
      targetClasses: target?.className,
      targetDisplay: target ? window.getComputedStyle(target).display : null,
      targetHeight: target?.offsetHeight,
      targetCat: target?.dataset?.cat,
      targetInfoHeight: target?.querySelector('.p-info')?.offsetHeight,
      targetInfoDisplay: target?.querySelector('.p-info') ? window.getComputedStyle(target.querySelector('.p-info')).display : null,
      targetAllInfoKids: target ? Array.from(target.querySelector('.p-info').children).map(c => ({
        cls: c.className, text: c.textContent.trim().substring(0,30), 
        h: c.offsetHeight, w: c.offsetWidth
      })) : null
    };
  });
  
  fs.writeFileSync('debug2_initial.json', JSON.stringify(initial, null, 2));
  fs.writeFileSync('debug2_afterClickAll.json', JSON.stringify(afterClickAll, null, 2));
  fs.writeFileSync('debug2_errors.txt', errors.join('\n'));
  
  // Screenshot AFTER clicking 全部
  await page.screenshot({ path: 'debug2_all.png', fullPage: false });
  // Scroll to products and screenshot
  await page.evaluate(() => document.getElementById('products')?.scrollIntoView());
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: 'debug2_products.png', fullPage: false });
  
  // Click 醬汁配料 and screenshot
  await page.click('.ct .t-btn[data-cat="醬汁配料"]');
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: 'debug2_醬汁配料.png', fullPage: false });
  
  await browser.close();
  console.log('Initial:', JSON.stringify(initial));
  console.log('After click 全部:', JSON.stringify(afterClickAll, null, 2));
  console.log('Errors:', errors.length);
})();
