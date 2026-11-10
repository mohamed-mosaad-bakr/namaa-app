#!/usr/bin/env python3
"""Namaa release helper — run from the repo root:
    python3 tools/release.py <build> <version> "<notes>"
e.g. python3 tools/release.py 273 27.3 "وصف قصير للتحديث"

It (1) bumps window.NM_BUILD in index.html, (2) checks every inline <script> with `node --check`,
(3) refuses the release if the ‹ › glyphs are present, or if any word listed in the local,
git-ignored file `.leakwords` (one per line: real asset names, keys...) appears in index.html,
(4) writes version.json. It does not commit or push.
"""
import json, os, re, subprocess, sys, tempfile

def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    build, ver, notes = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    html = open('index.html', encoding='utf-8').read()
    html, n = re.subn(r'window\.NM_BUILD=\d+;', 'window.NM_BUILD=%d;' % build, html)
    if n != 1:
        sys.exit('expected exactly one window.NM_BUILD=<n>; in index.html, found %d' % n)
    html, n = re.subn(r"window\.NM_VERSION='[^']*';", "window.NM_VERSION='%s';" % ver, html)
    if n != 1:
        sys.exit("expected exactly one window.NM_VERSION='..'; in index.html, found %d" % n)
    bad = [g for g in ('\u2039', '\u203a') if g in html]
    if bad:
        sys.exit('refusing: ‹ / › glyph found — use an inline SVG chevron instead')
    if os.path.exists('.leakwords'):
        for w in [l.strip() for l in open('.leakwords', encoding='utf-8') if l.strip()]:
            if w in html:
                sys.exit('refusing: a word from .leakwords is in index.html')
    scripts = [s for s in re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', html, re.S) if s.strip()]
    for i, code in enumerate(scripts):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(code)
        r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
        os.unlink(f.name)
        if r.returncode:
            sys.exit('node --check failed on script #%d:\n%s' % (i, r.stderr[-1500:]))
    open('index.html', 'w', encoding='utf-8').write(html)
    json.dump({'build': build, 'version': ver, 'size': len(html.encode('utf-8')), 'notes': notes},
              open('version.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print('ok: %d scripts checked, build %d (%s)' % (len(scripts), build, ver))

main()
