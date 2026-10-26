# -*- coding: utf-8 -*-
"""Wyciąga treść wszystkich stron i wpisów z finezja.org (zrzut API WP w _src/wp/) do _src/tresci.json.
Bloki: h2..h4, p, ul, faq (q/a), table (rows), img (src/alt), btn (x/href). Zrzut: 2026-10-26."""
import json, os, re, html
from bs4 import BeautifulSoup, NavigableString, Tag

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://www.finezja.org/'
SKIP = {'script', 'style', 'noscript', 'form', 'select', 'button', 'svg', 'iframe'}

def norm(s):
    s = s.replace(' ', ' ').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', s).strip()

def inline(el):
    """Tekst z zachowaniem <b> i linków wewnętrznych."""
    out = ''
    for c in el.children:
        if isinstance(c, NavigableString):
            out += html.escape(str(c), quote=False)
        elif isinstance(c, Tag):
            if c.name in SKIP: continue
            if c.name == 'br': out += '<br>'
            elif c.name in ('strong', 'b'):
                t = inline(c)
                out += f'<b>{t}</b>' if norm(re.sub('<[^>]+>', '', t)) else t
            elif c.name == 'a' and c.get('href'):
                href = c['href']
                t = inline(c)
                if href.startswith(SITE): href = '/' + href[len(SITE):]
                out += f'<a href="{html.escape(href)}">{t}</a>' if norm(t) else ''
            else:
                out += inline(c)
    out = re.sub(r'[ \t\r\n ]+', ' ', out)
    out = re.sub(r'\s*<br>\s*', '<br>', out).strip()
    out = re.sub(r'^(<br>)+|(<br>)+$', '', out)
    return out

def plain(x): return norm(re.sub('<[^>]+>', ' ', x))

def walk(el, out):
    for c in el.children:
        if not isinstance(c, Tag): continue
        n = c.name
        cls = ' '.join(c.get('class', []))
        if n in SKIP: continue
        if 'faq__accordionSingle' == cls.strip():
            q = c.select_one('.faq__accordionSingleTitle'); a = c.select_one('.faq__accordionSingleContent')
            if q and a:
                out.append({'t': 'faq', 'q': plain(inline(q)), 'a': [inline(p) for p in a.find_all(['p', 'li']) if plain(inline(p))] or [inline(a)]})
            continue
        if 'elementor-accordion-item' in cls or 'elementor-toggle-item' in cls:
            q = c.select_one('.elementor-tab-title'); a = c.select_one('.elementor-tab-content')
            if q and a:
                out.append({'t': 'faq', 'q': plain(inline(q)), 'a': [inline(p) for p in a.find_all(['p', 'li']) if plain(inline(p))] or [inline(a)]})
            continue
        if n == 'details':
            q = c.find('summary')
            if q:
                q.extract()
                out.append({'t': 'faq', 'q': plain(inline(q)), 'a': [inline(p) for p in c.find_all(['p', 'li']) if plain(inline(p))] or [inline(c)]})
            continue
        if n in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            t = inline(c)
            if plain(t): out.append({'t': n, 'x': t})
            continue
        if n == 'p':
            # przyciski w akapicie
            btns = c.select('a.o-btn, a.elementor-button')
            if btns and not plain(''.join(str(s) for s in c.find_all(string=True, recursive=False))):
                for b in btns: out.append({'t': 'btn', 'x': plain(b.get_text()), 'href': b.get('href', '')})
                continue
            t = inline(c)
            if plain(t): out.append({'t': 'p', 'x': t})
            for im in c.find_all('img'): add_img(im, out)
            continue
        if n in ('ul', 'ol'):
            items = [inline(li) for li in c.find_all('li', recursive=False)]
            items = [i for i in items if plain(i)]
            if items: out.append({'t': 'ul', 'x': items})
            continue
        if n == 'table':
            rows = []
            for tr in c.find_all('tr'):
                cells = [inline(td) for td in tr.find_all(['td', 'th'])]
                if any(plain(x) for x in cells): rows.append(cells)
            if rows: out.append({'t': 'table', 'rows': rows})
            continue
        if n == 'img':
            add_img(c, out); continue
        if n == 'a' and ('o-btn' in cls or 'elementor-button' in cls):
            out.append({'t': 'btn', 'x': plain(c.get_text()), 'href': c.get('href', '')}); continue
        if n == 'div' and 'elementor-counter' in cls:
            num = c.select_one('.elementor-counter-number'); tit = c.select_one('.elementor-counter-title')
            if num:
                out.append({'t': 'counter', 'x': (num.get('data-to-value') or plain(num.get_text())), 'pre': plain(c.select_one('.elementor-counter-number-prefix').get_text()) if c.select_one('.elementor-counter-number-prefix') else '',
                            'suf': plain(c.select_one('.elementor-counter-number-suffix').get_text()) if c.select_one('.elementor-counter-number-suffix') else '', 'label': plain(tit.get_text()) if tit else ''})
            continue
        # elementor tekst w div bez <p>
        if n == 'div' and 'elementor-widget-container' in cls and not c.find(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'img', 'div']):
            t = inline(c)
            if plain(t): out.append({'t': 'p', 'x': t})
            continue
        walk(c, out)

def add_img(im, out):
    src = im.get('data-src') or im.get('src') or ''
    if not src or src.startswith('data:'): return
    src = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', src)
    out.append({'t': 'img', 'src': src, 'alt': norm(im.get('alt', ''))})

def blocks(h):
    s = BeautifulSoup(h, 'html.parser'); out = []
    walk(s, out)
    ded = []
    for b in out:
        if ded and b == ded[-1]: continue
        ded.append(b)
    return ded

res = {}
for fn, kind in (('pages_full.json', 'page'), ('posts_full.json', 'post')):
    for x in json.load(open(os.path.join(HERE, 'wp', fn), encoding='utf-8')):
        path = x['link'].replace(SITE, '')
        res[path] = {'kind': kind, 'title': html.unescape(x['title']['rendered']), 'slug': x['slug'], 'date': x['date'][:10],
                     'modified': x['modified'][:10], 'parent': x.get('parent', 0), 'cats': x.get('categories', []),
                     'excerpt': plain(html.unescape(x.get('excerpt', {}).get('rendered', ''))),
                     'yoast': {k: (x.get('yoast_head_json') or {}).get(k) for k in ('title', 'description', 'og_image')},
                     'blocks': blocks(x['content']['rendered'])}
json.dump(res, open(os.path.join(HERE, 'tresci.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
with open(os.path.join(HERE, 'tresci.txt'), 'w', encoding='utf-8') as f:
    for k, v in res.items():
        f.write(f'\n######## /{k} | {v["title"]} | {v["kind"]} | {v["date"]}\n')
        for b in v['blocks']:
            t = b['t']
            if t == 'ul': f.write('  - ' + '\n  - '.join(b['x']) + '\n')
            elif t == 'faq': f.write(f'[Q] {b["q"]}\n[A] ' + ' / '.join(b['a']) + '\n')
            elif t == 'table': f.write('[table]\n' + '\n'.join('  | ' + ' | '.join(r) for r in b['rows']) + '\n')
            elif t == 'img': f.write(f'[img] {b["src"]} | {b["alt"]}\n')
            elif t == 'btn': f.write(f'[btn] {b["x"]} -> {b["href"]}\n')
            elif t == 'counter': f.write(f'[counter] {b["pre"]}{b["x"]}{b["suf"]} {b["label"]}\n')
            else: f.write(f'[{t}] {b["x"]}\n')
print(len(res), 'stron;', sum(len(v['blocks']) for v in res.values()), 'bloków')
