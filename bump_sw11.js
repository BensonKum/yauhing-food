const fs = require('fs');
let h = fs.readFileSync('service-worker.js', 'utf8');
h = h.replace('yauhing-inventory-v10', 'yauhing-inventory-v11');
fs.writeFileSync('service-worker.js', h);
console.log('SW bumped to v11');
