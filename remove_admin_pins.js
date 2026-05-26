const admin = require('firebase-admin');
const serviceAccount = require('./firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: 'yauhing-food'
});

const db = admin.firestore();

async function removeAdminPins() {
  console.log('=== 刪除 Admin PIN 欄位 ===\n');

  // Jimmy's document
  const jimmySnapshot = await db.collection('employees')
    .where('name', '==', 'Jimmy')
    .get();

  if (jimmySnapshot.empty) {
    console.log('Jimmy document not found');
  } else {
    const jimmyDoc = jimmySnapshot.docs[0];
    console.log('Jimmy:', jimmyDoc.id, jimmyDoc.data());
    await jimmyDoc.ref.update({ pin: admin.firestore.FieldValue.delete() });
    console.log('✅ Jimmy PIN deleted\n');
  }

  // 容's document
  const docId = 'emp_1778497359685_fzz9mo';
  const yungDoc = await db.collection('employees').doc(docId).get();
  console.log('容:', docId, yungDoc.data());
  await yungDoc.ref.update({ pin: admin.firestore.FieldValue.delete() });
  console.log('✅ 容 PIN deleted\n');

  console.log('=== 完成 ===');
  process.exit();
}

removeAdminPins().catch(err => { console.error('Error:', err); process.exit(1); });