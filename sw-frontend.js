/**
 * 祐興食品前台 — Service Worker
 * 提供離線緩存功能（PWA）
 */

const CACHE_NAME = 'yauhing-frontend-v6';

// 需要緩存的靜態資源
const urlsToCache = [
  '/',
  '/index.html',
  '/products_v2.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/icon-maskable-192x192.png',
  '/icons/icon-maskable-512x512.png',
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
        // 逐條加入，避免一條失敗全部reject
        return Promise.all(
          urlsToCache.map(url =>
            fetch(url, { mode: 'cors' })
              .then(resp => {
                if (resp.ok) return cache.put(url, resp);
              })
              .catch(err => console.warn('[SW] Cache skip:', url, err))
          )
        );
      })
      .then(() => console.log('[SW Frontend] Cache ready'))
      .catch(error => {
        console.warn('[SW Frontend] Cache partial fail (non-fatal):', error);
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
 * 攔截請求：網絡優先（新策略）
 * - 先 fetch 最新版本
 * - 如果成功，cache 起來
 * - 如果失敗，fallback 到 cache
 */
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // 網絡成功，cache起來
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        console.log('[SW Frontend] Network fetch OK:', event.request.url);
        return response;
      })
      .catch(() => {
        // 網絡失敗，fallback 到 cache
        return caches.match(event.request).then(cached => {
          if (cached) {
            console.log('[SW Frontend] Serving from cache (offline):', event.request.url);
            return cached;
          }
          console.warn('[SW Frontend] No cache for:', event.request.url);
        });
      })
  );
});
