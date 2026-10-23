# namaa-app — release channel for the Namaa Android app

The Namaa APK (WebView) checks `version.json` here on launch. If `build` is higher than its own
`NM_BUILD`, it downloads `index.html`, saves it on the phone, and offers "حدّث دلوقتي".

Release rules:
- `index.html` must never contain personal portfolio data (no seed / migration IIFEs with asset names or values). User data lives only in the phone's localStorage.
- Bump BOTH `window.NM_BUILD=<n>;` inside index.html and `"build": <n>` in version.json. The app rejects a download whose HTML doesn't contain `NM_BUILD=<n>;`.
- The main app script (the `<script>` containing `InvestmentCalculator`) must pass `node --check` with paren balance 0 before pushing (a broken release is auto-rolled back on next launch, but avoid it).
- Native changes (Bridge / MainActivity) still need a new APK.
- Never use the `‹` / `›` glyphs for arrows/chevrons — in RTL text they get bidi-mirrored and point the wrong way. Use an inline SVG chevron (`<path d="m15 18-6-6 6-6"/>` = forward/left, `m9 18 6-6-6-6` = back/right). `make_release.py` refuses to build if either glyph is in the release.
