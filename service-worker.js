/**
 * 祐興倉存系統 — Service Worker
 * 提供離線緩存功能
 */

const CACHE_NAME = 'yauhing-inventory-v9'; // v8: skipWaiting+clients.claim; v9: SW URL cache-bust + CACHE bump

// 需要緩存的靜態資源
const urlsToCache = [
  '/inventory.html',
  '/manifest-inventory.json',
  '/icon-warehouse-192.png',
  '/icon-warehouse-512.png',
  '/images/product_corn_dumpling.jpg',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore-compat.js',
  'https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js'
];

/**
 * 安裝事件：緩存靜態資源
 */
self.addEventListener('install', event => {
  console.log('[Service Worker] Install v7');
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
  // 立即接管，不等舊 SW 嘅 clients 關晒
  self.skipWaiting();
});

/**
 * 攔截請求：優先使用緩存
 */
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  const isHtml = event.request.mode === 'navigate' || url.pathname.endsWith('.html');
  const isProducts = url.pathname.endsWith('products_v2.json');

  // Network-first for HTML pages AND products.json（產品目錄經常改，唔可以 cache 舊版）
  if (isHtml || isProducts) {
    event.respondWith(
      fetch(event.request, isProducts ? {cache:'no-store'} : undefined)
        .then(response => {
          // HTML 可 cache 作離線用；products.json 永遠唔 cache（避免 SW 派發舊版）
          if (response && response.status === 200 && !isProducts) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }
  // Cache-first for static assets (JS libs etc.)
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request).then(response => {
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseToCache));
          return response;
        });
      })
      .catch(error => {
        console.error('[Service Worker] Fetch failed:', error);
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
