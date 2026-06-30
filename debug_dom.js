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
  
  // Capture console errors
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push('CONSOLE: ' + msg.text());
  });
  page.on('pageerror', err => errors.push('PAGEERROR: ' + err.message));
  
  await page.goto('file:///C:/Users/user/.qclaw/workspace/yauhing-food/index.html', { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 1500));
  
  // Find 醬油套裝 card and dump its full structure
  const result = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.p-card'));
    const target = cards.find(c => c.querySelector('.p-name')?.textContent.trim() === '醬油套裝');
    const ref = cards.find(c => c.querySelector('.p-name')?.textContent.trim() === '稻米油');
    
    function dumpCard(card) {
      if (!card) return null;
      const info = card.querySelector('.p-info');
      const infoStyle = info ? window.getComputedStyle(info) : null;
      const cardStyle = window.getComputedStyle(card);
      return {
        cardHTML: card.outerHTML,
        cardRect: card.getBoundingClientRect(),
        cardHeight: card.offsetHeight,
        infoExists: !!info,
        infoChildrenCount: info ? info.children.length : 0,
        infoChildrenHTML: info ? Array.from(info.children).map(c => ({
          tag: c.tagName, cls: c.className, text: c.textContent.trim().substring(0,30),
          offsetHeight: c.offsetHeight, display: window.getComputedStyle(c).display,
          visibility: window.getComputedStyle(c).visibility, opacity: window.getComputedStyle(c).opacity
        })) : [],
        infoRect: info ? info.getBoundingClientRect() : null,
        infoHeight: info ? info.offsetHeight : null,
        infoComputedHeight: infoStyle ? infoStyle.height : null,
        infoComputedMinHeight: infoStyle ? infoStyle.minHeight : null,
        cardComputedAlignSelf: cardStyle.alignSelf,
        cardComputedHeight: cardStyle.height,
        cardDisplay: cardStyle.display,
        cardFlexDir: cardStyle.flexDirection,
        pNote: card.querySelector('.p-note') ? {
          text: card.querySelector('.p-note').textContent.trim(),
          height: card.querySelector('.p-note').offsetHeight,
          computedHeight: window.getComputedStyle(card.querySelector('.p-note')).height,
          margin: window.getComputedStyle(card.querySelector('.p-note')).margin
        } : null
      };
    }
    return {
      targetCard: dumpCard(target),
      refCard: dumpCard(ref),
      totalCards: cards.length,
      sameRowAsTarget: target ? target.previousElementSibling?.className : null
    };
  });
  
  fs.writeFileSync('debug_result.json', JSON.stringify(result, null, 2));
  fs.writeFileSync('debug_errors.txt', errors.join('\n'));
  
  // Take screenshot of the 醬油套裝 area
  const target = await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.p-card'));
    const t = cards.find(c => c.querySelector('.p-name')?.textContent.trim() === '醬油套裝');
    return t ? { x: t.getBoundingClientRect().x, y: t.getBoundingClientRect().y, 
                 w: t.getBoundingClientRect().width, h: t.getBoundingClientRect().height,
                 x2: t.previousElementSibling ? t.previousElementSibling.getBoundingClientRect().x : null,
                 prevName: t.previousElementSibling?.querySelector('.p-name')?.textContent } : null;
  });
  if (target) {
    await page.screenshot({ 
      path: 'debug_target.png',
      clip: { x: Math.max(0, target.x - 20), y: Math.max(0, target.y - 20), 
              width: target.w * 2 + 40, height: target.h + 40 }
    });
    // Also full screenshot
    await page.screenshot({ path: 'debug_fullpage.png', fullPage: false });
  }
  
  await browser.close();
  console.log('Done. Errors:', errors.length);
  console.log('Target card info:', JSON.stringify(result.targetCard, null, 2));
})();
