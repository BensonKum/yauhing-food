const admin = require('firebase-admin');
const fs = require('fs');

// 讀取 Service Account Key
const serviceAccount = JSON.parse(fs.readFileSync('./firebase-service-account.json', 'utf8'));

// 初始化 Firebase Admin
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const email = 'inamyleung@yahoo.com.hk';
const password = 'il2450';

async function createUser() {
  try {
    // 建立用戶
    const userRecord = await admin.auth().createUser({
      email: email,
      password: password,
      displayName: '容'
    });
    
    console.log(`✅ 成功！用戶已建立：`);
    console.log(`   UID: ${userRecord.uid}`);
    console.log(`   Email: ${email}`);
    console.log(`   密碼: ${password}`);
    console.log(`\n請手動將以下資料加入 Firestore employees collection：`);
    console.log(`   document ID: ${userRecord.uid}`);
    console.log(`   data: { name: "容", email: "${email}", role: "admin", store: "both", pin: "92782450" }`);
  } catch (error) {
    if (error.code === 'auth/email-already-exists') {
      console.error('❌ Email 已存在，嘗試更新密碼...');
      try {
        const user = await admin.auth().getUserByEmail(email);
        await admin.auth().updateUser(user.uid, { password: password });
        console.log(`✅ 成功！用戶 ${email} 密碼已更新為 ${password}`);
        console.log(`   UID: ${user.uid}`);
      } catch (e2) {
        console.error('❌ 更新失敗：', e2.message);
      }
    } else {
      console.error('❌ 錯誤：', error.message);
    }
  } finally {
    process.exit(0);
  }
}

createUser();
