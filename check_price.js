const fs = require('fs');
const h = fs.readFileSync('inventory.html', 'utf8');
const lines = h.split('\n');
lines.forEach((l, i) => {
  if (l.includes('pcard-add') || l.includes('btn-add') || l.includes('HK$') || (l.includes('price') && l.includes('text'))) {
    console.log(i + 1, l.trim().substring(0, 250));
  }
});
