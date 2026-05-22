import shutil
import os
import datetime

src = r'C:\Users\admin\.qclaw\workspace\yauhing-food'
backup_root = r'C:\Users\admin\Desktop\QClaw\備份\祐興網站'

# 建立備份根目錄
os.makedirs(backup_root, exist_ok=True)

# 產生時間戳記
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
dest = os.path.join(backup_root, timestamp)

print('來源: ' + src)
print('備份至: ' + dest)

if not os.path.exists(src):
    print('錯誤：來源目錄不存在')
else:
    # 執行備份
    shutil.copytree(src, dest)
    
    # 計算檔案數量和大小
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(dest):
        total_files += len(files)
        for f in files:
            fp = os.path.join(root, f)
            total_size += os.path.getsize(fp)
    
    size_kb = total_size // 1024
    print('備份完成：' + str(total_files) + ' 個檔案，' + str(size_kb) + ' KB')
    print('備份路徑: ' + dest)
