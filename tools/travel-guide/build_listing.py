# -*- coding: utf-8 -*-
"""Builds the Russian Travel Guide listing (/ru/travel-guide) from the English
listing source (travel-guide.html) and makes the English page language-fixed.

Run: python tools/travel-guide/build_listing.py   (then build_article.py)

travel-guide.html is the source of truth: write/edit it in English with
data-en / data-ru attributes; this script resolves every data-ru string into
real static Russian text so the Russian URL is fully indexable.
"""
import os, re
from html import escape, unescape

SCR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCR, "..", ".."))
SITE = "https://yourguideuz.com"
EN_PATH, RU_PATH = "/travel-guide", "/ru/travel-guide"

TITLE_RU = "Путеводитель по Узбекистану — YourGuideUz | Города, советы и маршруты"
DESC_RU = "Планируйте поездку в Узбекистан: лучшие города, визы, деньги, поезда, SIM-карты, культурные советы и готовые маршруты на 5, 7 и 10+ дней по Шёлковому пути."

HEAD_SEO = '''<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{en}">
<link rel="alternate" hreflang="ru" href="{ru}">
<link rel="alternate" hreflang="x-default" href="{en}">
'''.format(canon="{canon}", en=SITE + EN_PATH, ru=SITE + RU_PATH)

def read(p):
    return open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")

def ensure_en_page(s):
    """Idempotently make the English page language-fixed with canonical + hreflang."""
    if "data-fixed-lang" not in s:
        s = s.replace('<body data-page="travel-guide" class="page-header">',
                      '<body data-page="travel-guide" data-fixed-lang class="page-header">', 1)
    if 'rel="canonical"' not in s:
        s = s.replace('<link rel="icon"', HEAD_SEO.format(canon=SITE + EN_PATH) + '<link rel="icon"', 1)
    return s

LEAF = re.compile(
    r'<(?P<tag>[a-zA-Z0-9]+)(?P<pre>[^<>]*?)\sdata-en="(?P<en>[^"]*)"\sdata-ru="(?P<ru>[^"]*)"(?P<post>[^<>]*)>(?P<body>[^<]*)</(?P=tag)>')

def to_russian(s):
    def leaf(m):
        txt = escape(unescape(m.group("ru")), quote=False)
        return f'<{m.group("tag")}{m.group("pre")} data-en="{m.group("en")}" data-ru="{m.group("ru")}"{m.group("post")}>{txt}</{m.group("tag")}>'
    s = LEAF.sub(leaf, s)
    # <meta content> pairs
    s = re.sub(r'(<meta name="description" content=")[^"]*(" data-en-content="[^"]*" data-ru-content=")([^"]*)(">)',
               lambda m: m.group(1) + m.group(3) + m.group(2) + m.group(3) + m.group(4), s)
    # links that differ per language
    s = re.sub(r'href="[^"]*"(\s+)data-en-href="[^"]*"(\s+)data-ru-href="([^"]*)"',
               lambda m: f'href="{m.group(3)}"{m.group(1)}data-en-href="{m.group(3)}"{m.group(2)}data-ru-href="{m.group(3)}"', s)
    # absolute asset / page paths (served from /ru/...)
    s = re.sub(r'href="index\.html"', 'href="/"', s)
    s = re.sub(r'href="(?!https?:|/|#|mailto:|tel:)([^"]+)"', r'href="/\1"', s)
    s = re.sub(r'src="(assets|images)/', r'src="/\1/', s)
    # language + canonical + hreflang
    s = s.replace('<html lang="en">', '<html lang="ru">', 1)
    s = s.replace(f'<link rel="canonical" href="{SITE + EN_PATH}">', f'<link rel="canonical" href="{SITE + RU_PATH}">', 1)
    # Travel Guide links stay inside the Russian section
    s = s.replace('href="/travel-guide"', f'href="{RU_PATH}"')
    # header language buttons: Russian is the active one
    s = s.replace('data-lang="en" class="active"', 'data-lang="en"')
    s = re.sub(r'data-lang="ru">', 'data-lang="ru" class="active">', s)
    return s

def main():
    p = os.path.join(ROOT, "travel-guide.html")
    en = ensure_en_page(read(p))
    open(p, "w", encoding="utf-8", newline="\n").write(en)
    ru = to_russian(en)
    out = os.path.join(ROOT, "articles", "ru", "travel-guide.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(ru)
    print("ok", len(en), len(ru))

if __name__ == "__main__":
    main()
