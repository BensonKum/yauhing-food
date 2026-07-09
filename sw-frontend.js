/**
 * 祐興食品前台 — Service Worker
 * 提供離線緩存功能（PWA）
 */

const CACHE_NAME = 'yauhing-frontend-v1';

// 需要緩存的靜態資源
const urlsToCache = [
  '/',
  '/index.html',
  '/products_v2.json',
  '/icons/icon-192x192.png',
  '/icons/logo.png',
  '/manifest.json'
];

/**
 * 安裝事件：緩存靜態資源
 */
self.addEventListener('install', event => {
  console.log('[SW Frontend] Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW Frontend] Caching all');
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.error('[SW Frontend] Cache failed:', error);
      })
  );
});

/**
 * 激活事件：清理舊緩存
 */
self.addEventListener('activate', event => {
  console.log('[SW Frontend] Activate');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW Frontend] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
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
          console.log('[SW Frontend] Serving from cache:', event.request.url);
          return response;
        }

        // 從網絡獲取，並緩存新資源
        return fetch(event.request).then(response => {
          // 檢查是否返回有效響應
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // 複製響應（流只能讀一次）
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      })
      .catch(error => {
        console.error('[SW Frontend] Fetch failed:', error);
        // 可以返回離線頁面
      })
  );
});
