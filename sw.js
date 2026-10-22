/* Namaa SW: network-first للصفحة (عشان التحديثات توصل فورًا)، والنسخة المحفوظة لو مفيش نت */
var C='nm-shell-v1';
self.addEventListener('install',function(){self.skipWaiting();});
self.addEventListener('activate',function(e){e.waitUntil(self.clients.claim());});
self.addEventListener('fetch',function(e){
 var r=e.request;if(r.method!=='GET'||r.mode!=='navigate')return;
 e.respondWith(fetch(r).then(function(res){if(res&&res.ok){var c=res.clone();caches.open(C).then(function(k){k.put('./',c);});}return res;}).catch(function(){return caches.match('./').then(function(m){return m||Response.error();});}));
});
