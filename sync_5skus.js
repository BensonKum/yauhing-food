const fs = require('fs');
const data = JSON.parse(fs.readFileSync('./products_v2.json', 'utf8'));
const admin = require('firebase-admin');
const serviceAccount = require('../../firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

const skus = ['YH402', 'YH403', 'YH404', 'YH405', 'YH406'];
const items = data.filter(x => skus.includes(x.sku));

async function addDocs() {
  for (const i of items) {
    await db.collection('products').doc(i.name).set({
      name: i.name,
      sku: i.sku,
      cat: i.cat,
      price: i.price,
      stock: 0,
      updatedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log('Added:', i.sku, '-', i.name);
  }
  console.log('All done!');
  process.exit(0);
}

addDocs().catch(e => { console.error(e); process.exit(1); });
