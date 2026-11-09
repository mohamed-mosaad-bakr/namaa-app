# namaa-app — release channel for the Namaa Android app

The Namaa APK (WebView) checks `version.json` here on launch. If `build` is higher than its own
`NM_BUILD`, it downloads `index.html`, saves it on the phone, and offers "حدّث دلوقتي".

Release rules:
- `index.html` must never contain personal portfolio data (no seed / migration IIFEs with asset names or values). User data lives only in the phone's localStorage.
- Bump BOTH `window.NM_BUILD=<n>;` inside index.html and `"build": <n>` in version.json. The app rejects a download whose HTML doesn't contain `NM_BUILD=<n>;`.
- The main app script (the `<script>` containing `InvestmentCalculator`) must pass `node --check` with paren balance 0 before pushing (a broken release is auto-rolled back on next launch, but avoid it).
- Native changes (Bridge / MainActivity) still need a new APK.
- Never use the `‹` / `›` glyphs for arrows/chevrons — in RTL text they get bidi-mirrored and point the wrong way. Use an inline SVG chevron (`<path d="m15 18-6-6 6-6"/>` = forward/left, `m9 18 6-6-6-6` = back/right). `make_release.py` refuses to build if either glyph is in the release.

For architecture, modules, data keys, GA events, the release helper (`tools/release.py`) and the APK process, read `HANDOFF.md` first.

Working mode (owner's standing rule): planning and execution are separate.
- The repo pins `"model": "opusplan"` in `.claude/settings.json`: Opus in plan mode, Sonnet when executing.
- For any non-trivial change (new feature, redesign, anything touching data/sync/APK), start in plan mode: read HANDOFF.md, inspect the code, and present a short plan (what changes, where, risks, how it will be tested). Implement only after the owner approves the plan.
- Tiny changes (a word, a color, a one-line fix) can go straight to execution.
