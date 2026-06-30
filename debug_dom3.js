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
  await new Promise(r => setTimeout(r, 3000));

  // Step 1: click "醬汁配料"
  await page.evaluate(() => {
    const btns = document.querySelectorAll('.ct .t-btn');
    for (let b of btns) {
      if (b.dataset.cat === '醬汁配料') { b.click(); break; }
    }
  });
  await new Promise(r => setTimeout(r, 500));

  // Step 2: dump 醬油套裝 card state
  const sauceCard = await page.evaluate(() => {
    const all = document.querySelectorAll('.p-card');
    const target = Array.from(all).find(c => 
      c.querySelector('.p-name')?.textContent.trim() === '醬油套裝'
    );
    if (!target) return { error: '醬油套裝 not found' };
    
    const info = target.querySelector('.p-info');
    const img = target.querySelector('.p-img');
    const cardStyle = window.getComputedStyle(target);
    const infoStyle = info ? window.getComputedStyle(info) : null;
    
    return {
      classes: target.className,
      display: cardStyle.display,
      cardHeight: target.offsetHeight,
      cardRect: target.getBoundingClientRect(),
      img: img ? {
        height: img.offsetHeight,
        rect: img.getBoundingClientRect()
      } : null,
      info: info ? {
        height: info.offsetHeight,
        rect: info.getBoundingClientRect(),
        computedHeight: infoStyle.height,
        paddingTop: infoStyle.paddingTop,
        paddingBottom: infoStyle.paddingBottom,
        overflow: infoStyle.overflow,
        children: Array.from(info.children).map(c => ({
          tag: c.tagName,
          className: c.className,
          text: c.textContent.trim().substring(0, 40),
          height: c.offsetHeight,
          display: window.getComputedStyle(c).display,
          visibility: window.getComputedStyle(c).visibility,
          rect: c.getBoundingClientRect()
        }))
      } : null,
      // Also check the add-cart-btn specifically
      addBtn: target.querySelector('.add-cart-btn') ? {
        height: target.querySelector('.add-cart-btn').offsetHeight,
        text: target.querySelector('.add-cart-btn').textContent.trim().substring(0, 30),
        display: window.getComputedStyle(target.querySelector('.add-cart-btn')).display
      } : null
    };
  });

  // Step 3: also dump the 稻米油 card for comparison
  const riceCard = await page.evaluate(() => {
    const all = document.querySelectorAll('.p-card');
    const target = Array.from(all).find(c => 
      c.querySelector('.p-name')?.textContent.trim() === '稻米油'
    );
    if (!target) return { error: '稻米油 not found' };
    return {
      classes: target.className,
      display: window.getComputedStyle(target).display,
      cardHeight: target.offsetHeight,
      addBtn: target.querySelector('.add-cart-btn') ? {
        height: target.querySelector('.add-cart-btn').offsetHeight,
        display: window.getComputedStyle(target.querySelector('.add-cart-btn')).display
      } : null
    };
  });

  // Step 4: How many cards visible?
  const counts = await page.evaluate(() => {
    return {
      total: document.querySelectorAll('.p-card').length,
      hid: document.querySelectorAll('.p-card.hid').length,
      visible: document.querySelectorAll('.p-card:not(.hid)').length,
      醬油Visible: Array.from(document.querySelectorAll('.p-card:not(.hid)')).filter(c => c.dataset.cat === '醬汁配料').length
    };
  });

  // Screenshot
  await page.evaluate(() => document.getElementById('products')?.scrollIntoView());
  await new Promise(r => setTimeout(r, 500));
  await page.screenshot({ path: 'debug3_醬汁配料.png', fullPage: false });

  fs.writeFileSync('debug3_sauceCard.json', JSON.stringify(sauceCard, null, 2));
  fs.writeFileSync('debug3_riceCard.json', JSON.stringify(riceCard, null, 2));
  fs.writeFileSync('debug3_counts.json', JSON.stringify(counts, null, 2));
  fs.writeFileSync('debug3_errors.txt', errors.join('\n'));

  console.log('=== Counts ===');
  console.log(JSON.stringify(counts, null, 2));
  console.log('=== Sauce card ===');
  console.log(JSON.stringify(sauceCard, null, 2));
  console.log('=== Rice card ===');
  console.log(JSON.stringify(riceCard, null, 2));

  await browser.close();
})();
