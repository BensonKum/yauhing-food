/**
 * 祐興倉存系統 — Service Worker
 * 提供離線緩存功能
 */

const CACHE_NAME = 'yauhing-inventory-v2';

// 需要緩存的靜態資源
const urlsToCache = [
  '/',
  '/inventory.html',
  '/',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore-compat.js',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js'
];

/**
 * 安裝事件：緩存靜態資源
 */
self.addEventListener('install', event => {
  console.log('[Service Worker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching all');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('[Service Worker] Cache failed:', error);
      })
  );
});

/**
 * 攔截請求：優先使用緩存
 */
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // 如果緩存中有，返回緩存；否則從網絡獲取
        if (response) {
          console.log('[Service Worker] Serving from cache:', event.request.url);
          return response;
        }

        // 從網絡獲取，並緩存新資源
        return fetch(event.request).then(response => {
          // 檢查是否返回有效響應
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // 複製響應（因為 response 只能讀一次）
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      })
      .catch(error => {
        console.error('[Service Worker] Fetch failed:', error);
        // 可以返回一個離線 Fallback 頁面
      })
  );
});

/**
 * 激活事件：清理舊緩存
 */
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activate');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      // 立即接管所有頁面（不用等下次加載）
      return self.clients.claim();
    })
  );
});

/**
 * 監聽消息：強制跳過等待（立即激活新版本）
 */
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
