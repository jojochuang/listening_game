const CACHE_NAME = 'word-writing-cache-v2';
const STATIC_ASSETS = [
  './',
  './index.html',
  './listening_game.html',
  './worksheet_generator.html',
  './grid_paper_generator.html',
  './draw_interface.html',
  './stroke_checker.html',
  './simplified_stroke_generator.html',
  './svg_editor.html',
  './BpmfZihiOnly-R.ttf'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.method !== 'GET') {
    return;
  }

  // 優先回應快取中的靜態資源
  if (STATIC_ASSETS.some(path => url.pathname.endsWith(path.replace('./', '/')))) {
    event.respondWith(
      caches.match(req).then(cached => cached || fetch(req))
    );
    return;
  }

  // 圖片與音訊：先網路，失敗再用快取，並將成功結果寫入快取
  if (req.destination === 'image' || req.destination === 'audio') {
    event.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // 其他 GET：嘗試網路，失敗再快取
  event.respondWith(
    fetch(req).catch(() => caches.match(req))
  );
});

