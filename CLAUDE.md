# namaa-app — release channel for the Namaa Android app

The Namaa APK (WebView) checks `version.json` here on launch. If `build` is higher than its own
`NM_BUILD`, it downloads `index.html`, saves it on the phone, and offers "حدّث دلوقتي".

Release rules:
- `index.html` must never contain personal portfolio data (no seed / migration IIFEs with asset names or values). User data lives only in the phone's localStorage.
- Bump BOTH `window.NM_BUILD=<n>;` inside index.html and `"build": <n>` in version.json. The app rejects a download whose HTML doesn't contain `NM_BUILD=<n>;`.
- Script index 7 paren balance must stay 0 and `node --check` must pass before pushing (a broken release is auto-rolled back on next launch, but avoid it).
- Native changes (Bridge / MainActivity) still need a new APK.
