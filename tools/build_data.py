#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate assets/js/data.js from data/site-data.json.

The site reads its content from ``window.SITE_DATA`` (loaded with a plain
<script> tag) so that it also works when index.html is opened over file://.

Usage (from the repository root):
    python tools/build_data.py

The script also checks that every local asset referenced in the data exists
and prints a warning for each missing file.
"""
import hashlib
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'data', 'site-data.json')
OUT = os.path.join(ROOT, 'assets', 'js', 'data.js')


def iter_asset_paths(node):
    """Yield every string value that looks like a local asset path."""
    if isinstance(node, dict):
        for value in node.values():
            yield from iter_asset_paths(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_asset_paths(value)
    elif isinstance(node, str) and node.startswith('assets/'):
        yield node


def main():
    for stream in (sys.stdout, sys.stderr):  # never crash on consoles without UTF-8
        try:
            stream.reconfigure(errors='replace')
        except (AttributeError, ValueError):
            pass
    try:
        with io.open(SRC, encoding='utf-8') as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print('HATA / ERROR: %s okunamadı: %s' % (SRC, exc), file=sys.stderr)
        return 1

    missing = sorted({p for p in iter_asset_paths(data) if not os.path.isfile(os.path.join(ROOT, p))})
    for path in missing:
        print('UYARI / WARNING: dosya bulunamadı: %s' % path, file=sys.stderr)

    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    # keep the output safe even if the text ever contains "</script>"
    payload = payload.replace('</', '<\\/')
    banner = ('/* Bu dosya tools/build_data.py tarafından data/site-data.json dosyasından üretilir.\n'
              '   Elle düzenlemeyin. / Generated from data/site-data.json - do not edit by hand. */\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(banner)
        fh.write('window.SITE_DATA = ')
        fh.write(payload)
        fh.write(';\n')

    print('Yazıldı / written: %s (%d bayt / bytes, %d yayın, %d proje, %d patent)' % (
        os.path.relpath(OUT, ROOT), os.path.getsize(OUT), len(data.get('publications', [])),
        len(data.get('projects', [])), len(data.get('patents', []))))
    stamp_versions()
    return 0


VERSIONED = ('assets/css/main.css', 'assets/js/main.js', 'assets/js/data.js')
PAGES = ('index.html', '404.html')


def stamp_versions():
    """Append ?v=<content hash> to CSS/JS links so browsers never keep a stale copy."""
    hashes = {}
    for rel in VERSIONED:
        with open(os.path.join(ROOT, rel), 'rb') as fh:
            hashes[rel] = hashlib.sha1(fh.read()).hexdigest()[:10]
    for page in PAGES:
        path = os.path.join(ROOT, page)
        if not os.path.isfile(path):
            continue
        with io.open(path, encoding='utf-8') as fh:
            html = fh.read()
        new = html
        for rel, digest in hashes.items():
            new = re.sub(r'((?:href|src)="/?' + re.escape(rel) + r')(?:\?v=[0-9a-f]+)?"', r'\1?v=' + digest + '"', new)
        if new != html:
            with io.open(path, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(new)
    print('Sürüm etiketleri / cache-busting: ' + ', '.join('%s?v=%s' % (os.path.basename(k), v) for k, v in hashes.items()))


if __name__ == '__main__':
    sys.exit(main())
