const admin = require('firebase-admin');
const fs = require('fs');

// 讀取 Service Account Key
const serviceAccount = JSON.parse(fs.readFileSync('./firebase-service-account.json', 'utf8'));

// 初始化 Firebase Admin
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const email = 'jyvivi618@yahoo.com.hk';
const newPassword = 'jy8356';

async function changePassword() {
  try {
    // 用 email 搵用戶
    const userRecord = await admin.auth().getUserByEmail(email);
    console.log('找到用戶：', userRecord.uid);
    
    // 改密碼
    await admin.auth().updateUser(userRecord.uid, {
      password: newPassword
    });
    
    console.log(`✅ 成功！用戶 ${email} 密碼已改為 ${newPassword}`);
  } catch (error) {
    console.error('❌ 錯誤：', error.message);
  } finally {
    process.exit(0);
  }
}

changePassword();
