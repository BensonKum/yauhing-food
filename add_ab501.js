const fs = require('fs');
const path = 'products_v2.json';
let data = JSON.parse(fs.readFileSync(path, 'utf8'));

const newProducts = [
  {
    "cat": "罐頭/零售裝",
    "name": "鮑魚罐頭 (細罐)",
    "price": "HKD 28",
    "note": "",
    "stock": 0,
    "image": "",
    "img1": "鮑魚罐頭(細罐裝).jpg",
    "img2": "四個鮑魚罐頭細罐裝.jpg",
    "label1": "細罐",
    "label2": "四罐優惠",
    "local_img": "",
    "sku": "YH501",
    "sku_base": "YH501",
    "is_multi": false,
    "has_ab": false
  },
  {
    "cat": "罐頭/零售裝",
    "name": "鮑魚罐頭 (細罐)(四罐優惠)",
    "price": "HKD 100",
    "note": "",
    "stock": 0,
    "image": "",
    "img1": "鮑魚罐頭(細罐裝).jpg",
    "img2": "四個鮑魚罐頭細罐裝.jpg",
    "label1": "細罐",
    "label2": "四罐優惠",
    "local_img": "",
    "sku": "YH501A",
    "sku_base": "YH501",
    "is_multi": true,
    "has_ab": true
  }
];

newProducts.forEach(p => {
  const dup = data.find(d => d.sku === p.sku);
  if (dup) {
    console.log(`SKIP ${p.sku} - already exists`);
  } else {
    console.log(`ADD ${p.sku}: ${p.name} | ${p.price}`);
    data.push(p);
  }
});

fs.writeFileSync(path, JSON.stringify(data, null, 2), 'utf8');
console.log(`\nTotal: ${data.length} products`);
