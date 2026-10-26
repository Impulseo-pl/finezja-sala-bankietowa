# -*- coding: utf-8 -*-
"""Demo Finezja v4 – generator stron. python _src/build.py
Treść: _src/tresci.json (zrzut finezja.org z 26.10.2026, _src/wyciagnij.py). Te same adresy co na finezja.org."""
import json, os, re, html, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BASE = 'https://impulseo-pl.github.io/finezja-sala-bankietowa/'
T = json.load(open(os.path.join(HERE, 'tresci.json'), encoding='utf-8'))
TEL1, TEL1H = '665 188 619', '+48665188619'
TEL2, TEL2H = '601 637 397', '+48601637397'
MAIL = 'biuro@finezja.org'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Finezja+Sala+bankietowa+Kaczki+%C5%9Arednie+10c+Turek'
GOOGLE = 'https://maps.google.com/?cid=10082315392986740217'
FB = 'https://www.facebook.com/Finezja.sala.bankietowa'
IG = 'https://www.instagram.com/sala.bankietowa.finezja/'
YT = 'https://www.youtube.com/watch?v=g2kK5KW1re4'
LAT, LNG = 51.9715, 18.5210
V = '20261026'

# ---------------------------------------------------------------- obrazy
IMG = {}
for f in os.listdir(os.path.join(ROOT, 'img')):
    m = re.match(r'(.+)-(\d+)\.webp$', f)
    if not m: continue
    w, h = Image.open(os.path.join(ROOT, 'img', f)).size
    IMG.setdefault(m.group(1), []).append((w, h, f))
for k in IMG: IMG[k].sort()

def pic(p, name, alt, sizes='(max-width:1000px) 100vw, 50vw', lazy=True, cls='', extra=''):
    v = IMG[name]; w, h, f = v[-1]
    src = next((x for x in v if x[0] >= 1100), v[-1])[2]
    ss = ', '.join(f'{p}img/{x[2]} {x[0]}w' for x in v)
    la = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ''
    return f'<img src="{p}img/{src}" srcset="{ss}" sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}"{la}{c}{extra}>'

def big(p, name): return f'{p}img/{IMG[name][-1][2]}'

def fig(p, name, alt, cls='ph', fx='reveal', sizes='(max-width:1000px) 100vw, 50vw', cap=''):
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls} {fx}">{pic(p, name, alt, sizes)}</figure>{c}'

ALT = {
    'hero': 'Długie stoły z kwiatami pod lustrzanym sufitem w sali Finezja', 'sala-nowa': 'Sala bankietowa Finezja przygotowana na wesele – nakryte stoły i dekoracje kwiatowe',
    'sala-zyrandole': 'Kryształowe żyrandole i lustrzany sufit z oświetleniem LED', 'sala-kwiaty': 'Stoły weselne z kompozycjami kwiatowymi w Finezji',
    'sala-dluga': 'Długi stół weselny przez całą salę', 'sala-okna': 'Jasna sala z wysokimi oknami i stołami w rzędach', 'sala-stoly': 'Ustawienie stołów w rzędach w sali Finezja',
    'sala-wieczor': 'Sala Finezja wieczorem, przy przygaszonym świetle', 'sala-okragle': 'Okrągłe stoły i dekoracja z piór', 'sala-pion': 'Rzędy stołów pod lustrzanym sufitem',
    'scena-dj': 'Parkiet i stanowisko DJ-a w sali Finezja', 'bal-parkiet': 'Parkiet przygotowany na bal w Finezji', 'bal-sala': 'Sala Finezja ustawiona na bal',
    'bal-scianka': 'Ścianka i oświetlenie na balu w Finezji', 'stol-mlodych': 'Stół Pary Młodej z kwiatami', 'stol-gosci': 'Nakryty stół gości w sali Finezja',
    'dek-roze': 'Dekoracja z róż przy stole Pary Młodej', 'dek-kwiaty': 'Białe kwiaty przy stole Pary Młodej', 'dek-luk': 'Złoty łuk z kwiatami i napisem nad stołem Pary Młodej',
    'dek-mlodzi': 'Stół Pary Młodej z drewnianymi skrzynkami i świecami', 'dek-oltarz': 'Dekoracja kwiatowa na tle łukowego okna', 'dek-milosc': 'Neon „Miłość” przy stole Pary Młodej',
    'dek-balony': 'Ścianka z balonami i neonem w sali', 'dek-stol': 'Kwiaty na stole weselnym', 'nakrycie': 'Nakrycie stołu weselnego',
    'love': 'Podświetlany napis LOVE w ogrodzie przed salą', 'budynek-front': 'Budynek sali Finezja w Kaczkach Średnich', 'budynek-ogrod': 'Ogród i podjazd przed salą Finezja',
    'budynek-plac': 'Plac przed salą Finezja', 'budynek-wieczor': 'Budynek Finezji wieczorem', 'budynek-dzien': 'Sala Finezja w słoneczny dzień', 'wejscie': 'Wejście do sali bankietowej Finezja',
    'wieczor': 'Podświetlone wejście do sali Finezja wieczorem', 'slodki-stol': 'Słodki stół z deserami z własnej kuchni', 'slodki-babeczki': 'Babeczki, rurki i deserki na słodkim stole',
    'slodki-okno': 'Słodki stół przy oknie', 'slodki-regal': 'Regał z ciastami i deserami', 'kawa': 'Stanowisko z kawą i herbatą', 'catering-bufet': 'Bufet z przekąskami i ciastami przygotowany przez kuchnię Finezji',
    'chrzest-neon': 'Neon „Chrzest Święty” i balony', 'chrzest-balony': 'Dekoracja balonowa na chrzciny', 'chrzest-pion': 'Ścianka z neonem „Chrzest Święty” i fotelem',
    'osiemnastka': 'Ścianka z balonami i cyfrą 18 na osiemnastkę', 'urodziny-scianka': 'Cekinowa ścianka „Happy Birthday” z balonami', 'urodziny-50': 'Balony i cyfra 50 na jubileusz',
    'urodziny-pion': 'Dekoracja urodzinowa z balonami', 'scianka-mis': 'Ścianka z balonami i misiem', 'zespol': 'Zespół Finezji – kucharz i obsługa przy stole z przekąskami',
    'plakat-andrzejki': 'Plakat Bal Andrzejkowy 2026 – Sala Finezja, 21.11.2026, godz. 19:00, 220 zł/os.', 'plakat-karnawal': 'Plakat Bal Karnawałowy 2026 w Finezji',
    'plakat-noworoczny': 'Plakat Bal Noworoczny w Finezji', 'menu-catering-1': 'Menu cateringowe Finezji – ceny dań: zupy, mięsa, przekąski i sałatki',
    'menu-catering-2': 'Menu cateringowe Finezji – dodatki, ciasta, torty i deserki z cenami', 'menu-wigilia-firmowa': 'Wigilia firmowa 2026 – trzy zestawy menu świątecznego z cenami',
    'osiemnastka-kroki': 'Jak zorganizować osiemnastkę krok po kroku – grafika Finezji', 'kpo': 'Fundusze Europejskie, Rzeczpospolita Polska, Unia Europejska, Krajowy Plan Odbudowy',
}

# zdjęcia z finezja.org, które są prawdziwe (reszta to stock – zastępujemy zdjęciami sali)
RAWMAP = {'Bal_Andrzejkowy_2026_Plakat_1_-1.png': 'plakat-andrzejki', 'Bal_Karnawalowy_2026.png': 'plakat-karnawal', 'Bal_noworoczny_2025-2026.png': 'plakat-noworoczny',
          '2.png': 'menu-catering-1', 'catering-brudzew.webp': 'menu-catering-2', 'wigilia-firmowa-2026-menu-ceny-turek-1.webp': 'menu-wigilia-firmowa',
          'Jak-przygotowac-18-krok-po-kroku.webp': 'osiemnastka-kroki', '20241203_132533-1-1.webp': 'zespol', 'Sala-bankietowa-Finezja.webp': 'sala-nowa',
          'ile-kosztuje-catering-na-20-osob-widelki-cenowe-i-przyklady-1.webp': 'catering-bufet'}
POSTER = {'plakat-andrzejki', 'plakat-karnawal', 'plakat-noworoczny', 'menu-catering-1', 'menu-catering-2', 'menu-wigilia-firmowa', 'osiemnastka-kroki'}

# ---------------------------------------------------------------- treść: porządki po szkicach na finezja.org
FIX = [
    ('Dowozimy do [Turku, Konina, Koła, Kalisza – uzupełnij].', 'Dowozimy do Turku i okolic: Koło, Uniejów, Władysławów, Kawęczyn, Brudzew, Tuliszków.'),
    ('[ogród / staw / altana]', 'ogród z oczkiem wodnym'), ('ślub cywilny w plenerze [jeśli oferujecie]', 'ślub cywilny w plenerze'),
    ('Kaczki Średnie, [X] min pieszo', 'Kaczki Średnie, ok. 700 m'), ('<b>Wpłać zaliczkę</b> – [… zł/os.] blokuje miejsce;', '<b>Wpłać zaliczkę</b> – zaliczka blokuje miejsce;'),
    ('krzesełka do karmienia [2 szt]', 'krzesełka do karmienia (2 szt.)'), ('niemowlę [w toalecie damskiej]', 'niemowlę (w toalecie damskiej)'),
    ('<b>[białe/zielone]</b>', '<b>białe lub zielone</b>'), ('<b>[paczka ciasta cena 32 zł lub zestaw upominkowy 65 zł]</b>', '<b>(paczka ciasta 32 zł lub zestaw upominkowy 65 zł)</b>'),
    ('orientacyjnie149 złprzy', 'orientacyjnie 149 zł/os. przy'), ('minimum20 osób, przy cateringu10 osób', 'minimum 20 osób, przy cateringu 10 osób'),
    ('promieniu[30]km', 'promieniu 30 km'), ('zamówieniu,[bez dopłaty]', 'zamówieniu, bez dopłaty'),
    ('od 2010 roku <b>400</b> i wiemy', 'od 2010 roku – to już blisko <b>400</b> przyjęć – i wiemy'),
    ('gościliśmy spotkania wigilijne firm z Turku i okolic <b>70: zakłady produkcyjne, urzędy, szkoły.</b> – od 20-osobowych',
     'gościliśmy <b>70</b> spotkań wigilijnych firm z Turku i okolic – zakłady produkcyjne, urzędy, szkoły – od 20-osobowych'),
    ('od czwartku do niedzieli u. Kaczki Średnie 10c', 'od czwartku do niedzieli w Kaczkach Średnich 10c'), ('w Finezji,Kaczki', 'w Finezji, Kaczki'),
    ('Poza Turem', 'Poza Turkiem'), ('zł/os.]', 'zł/os.'), ('W Tureku', 'w Turku'), ('Finezja Sala Bankietowa przygotowuje', 'Finezja Sala Bankietowa przygotowuje'),
    ('Turku</b>lub <b>okolicy i</b>szukasz', 'Turku</b> lub <b>okolicy</b> i szukasz'), ('<b>sali</b><b>bankietowej</b>Finezja', '<b>sali bankietowej</b> Finezja'),
    ('<b>Kalisza</b>czy', '<b>Kalisza</b> czy'), ('<b>Kalisza</b>sprawia', '<b>Kalisza</b> sprawia'), ('Dziękujemy finesse', 'Dziękujemy Finezji'),
    ('piękniej przestrzeni', 'pięknej przestrzeni'), ('milo spędzisz', 'miło spędzisz'), ('zaangażowani,', 'zaangażowaniu,'),
    ('przygotuje<b>dania', 'przygotuje <b>dania'), ('Dostosowujemy<b>układ', 'Dostosowujemy <b>układ'), ('Finezji,<b>z dala', 'Finezji, <b>z dala'),
    ('Impreza rozpocznie się o godziny', 'Impreza rozpocznie się o godzinie'), ('lampkę szampan Dorato', 'lampkę szampana Dorato'),
    ('Przyjęcie dla [30–160] gości', 'Przyjęcie dla 30–160 gości'), ('dla [20–80] gości', 'dla 20–80 gości'),
]
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿️‍⭐✅✔✖]+')

def clean(t):
    for a, b in FIX: t = t.replace(a, b)
    t = EMOJI.sub('', t).replace('﻿', '')
    t = re.sub(r'\[([^\]\[]{1,40})\]', r'\1', t)               # [8] km -> 8 km
    t = t.replace('</b><b>', ' ')
    t = re.sub(r'</b>(?=[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż])', '</b> ', t)
    t = re.sub(r'([a-ząćęłńóśźż0-9\)])\.(?=[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż])', r'\1. ', t)
    t = re.sub(r'\s{2,}', ' ', t).replace(' ,', ',').strip()
    t = re.sub(r'^\s*[–-]\s*(?=<b>)', '', t)
    return t

def plain(t): return re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', html.unescape(t))).strip()

# ---------------------------------------------------------------- strony i nawigacja
OFERTA = [('wesele/', 'Wesele'), ('oferta/osiemnastka/', 'Osiemnastka'), ('oferta/urodziny/', 'Urodziny'), ('oferta/30-ste-urodziny/', '30. urodziny'),
          ('oferta/czterdziestka/', '40. urodziny'), ('oferta/komunia-swieta/', 'Komunia Święta'), ('oferta/chrzest/', 'Chrzest Święty'),
          ('oferta/spotkania-firmowe/', 'Spotkania firmowe'), ('oferta/konsolacja/', 'Konsolacja')]
CATER = [('catering-turek/', 'Catering z dowozem'), ('wigilia/', 'Catering wigilijny'), ('wigilia-firmowa/', 'Wigilia firmowa')]
BALE = [('andrzejki/', 'Bal Andrzejkowy 2026'), ('bal-noworoczny/', 'Bal Noworoczny'), ('karnawal/', 'Bal Karnawałowy')]
NAV = [('wesele/', 'Wesele', None), ('oferta/', 'Przyjęcia', [('oferta/', 'Wszystkie przyjęcia')] + OFERTA[1:]), ('catering-turek/', 'Catering', CATER),
       ('andrzejki/', 'Bale', BALE), ('galeria/', 'Galeria', None), ('kontakt-2/', 'O nas', None), ('blog/', 'Blog', None), ('kontakt/', 'Kontakt', None)]
POSTS = [k for k, v in T.items() if v['kind'] == 'post']
POSTS.sort(key=lambda k: T[k]['date'], reverse=True)
ALLP = set(T.keys())
LINKFIX = {'/menu-cateringowe-2026/': '/catering-turek/'}
CATNAME = {1: 'Blog', 15: 'Chrzciny', 16: 'Komunie', 18: 'Konsolacje', 17: 'Urodziny', 14: 'Wesela', 13: 'Wigilia', 20: 'Catering'}

def depth(path): return '../' * path.strip('/').count('/') + ('../' if path.strip('/') else '')

def links(t, p):
    def r(m):
        href = html.unescape(m.group(1))
        if href.startswith('/') and not href.startswith('//'):
            href = LINKFIX.get(href, href); k = href.lstrip('/')
            path, _, frag = k.partition('#')
            if path and path not in ALLP and not path.endswith('/') and path + '/' in ALLP: path += '/'
            if path not in ALLP and path != '': path = 'kontakt/'
            href = p + path + ('#' + frag if frag else '')
        return f'href="{html.escape(href)}"'
    return re.sub(r'href="([^"]*)"', r, t)

SVG_F = ('<svg viewBox="0 0 100 124" aria-hidden="true"><rect class="fr" x="1" y="1" width="98" height="122"/>'
         '<rect class="fr" x="7" y="7" width="86" height="110" style="stroke-width:.6"/>'
         '<text class="ff" x="50" y="88" text-anchor="middle" style="font:500 74px var(--serif)">F</text></svg>')
ICO = {
    'tel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>',
    'prev': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    'next': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>',
    'x': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>',
}

ORG = {
    "@type": ["EventVenue", "Restaurant"], "@id": BASE + "#finezja", "name": "Finezja – sala bankietowa",
    "description": "Sala weselna i bankietowa dla 60–160 gości w Kaczkach Średnich, 4 km od Turku. Własna kuchnia, catering, noclegi, bezpłatny parking. Od 2010 roku.",
    "url": BASE, "image": BASE + "img/" + IMG['sala-nowa'][-1][2], "telephone": TEL1H, "email": MAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Kaczki Średnie 10c", "postalCode": "62-700", "addressLocality": "Turek", "addressRegion": "wielkopolskie", "addressCountry": "PL"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG}, "maximumAttendeeCapacity": 160, "servesCuisine": "polska",
    "priceRange": "330–380 zł/os. (menu weselne 2026)", "vatID": "7391718282", "sameAs": [FB, IG],
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "10:00", "closes": "13:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Thursday", "opens": "09:00", "closes": "13:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Friday", "Saturday", "Sunday"], "opens": "09:00", "closes": "21:00"}],
}

def head(p, path, title, desc, ld=None, preload=None, og=None):
    lds = [ORG] + (ld or [])
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ''
    ogi = BASE + 'img/' + IMG[og or 'sala-nowa'][-1][2]
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL"><meta property="og:site_name" content="Finezja – sala bankietowa">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{ogi}"><meta property="og:url" content="{BASE}{path}">
<meta name="theme-color" content="#0e1320">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<script>(function(d){{d.className+=' js';try{{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;var s=sessionStorage;if(!s.getItem('fz_in'))d.className+=' d-closed d-intro';else if(s.getItem('fz_nav'))d.className+=' d-closed';}}catch(e){{}}}})(document.documentElement)</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600&family=Ibarra+Real+Nova:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/styles.css?v={V}">
{pre}
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": lds}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#tresc">Przejdź do treści</a>
<div class="doors" aria-hidden="true"><div class="door l"></div><div class="door r"></div>
<div class="doors-mark">{SVG_F}<span class="word">Finezja</span><span class="sub">sala bankietowa · Turek</span></div></div>
'''

def header(p, cur):
    li = []
    for href, lab, sub in NAV:
        on = ' aria-current="page"' if cur == href or (sub and any(cur == s[0] for s in sub)) else ''
        s = ''
        if sub: s = '<ul class="sub">' + ''.join(f'<li><a href="{p}{h}">{l}</a></li>' for h, l in sub) + '</ul>'
        li.append(f'<li><a href="{p}{href}"{on}>{lab}</a>{s}</li>')
    mli = []
    for href, lab, sub in NAV:
        s = f'<div class="msub">' + ''.join(f'<a href="{p}{h}">{l}</a>' for h, l in sub[1:] if True) + '</div>' if sub and len(sub) > 1 else ''
        mli.append(f'<li><a href="{p}{href}">{lab}</a>{s}</li>')
    return f'''<header class="head">
<div class="wrap">
<a class="brand" href="{p}" aria-label="Finezja – strona główna">{SVG_F}<span><b>Finezja</b><small>sala bankietowa · Turek</small></span></a>
<nav aria-label="Główna"><ul class="nav">{''.join(li)}</ul></nav>
<a class="head-tel" href="tel:{TEL1H}">{ICO['tel']}{TEL1}</a>
<a class="btn" href="{p}kontakt/#zapytanie">Zapytaj o termin</a>
<button class="burger" type="button" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>
</div>
</header>
<div class="mnav"><ul>{''.join(mli)}</ul>
<div class="mfoot"><a href="tel:{TEL1H}">{TEL1}</a><a href="tel:{TEL2H}">{TEL2}</a><a href="mailto:{MAIL}">{MAIL}</a><span>Kaczki Średnie 10c, 62-700 Turek</span></div></div>
'''

def footer(p):
    of = ''.join(f'<li><a href="{p}{h}">{l}</a></li>' for h, l in OFERTA)
    ca = ''.join(f'<li><a href="{p}{h}">{l}</a></li>' for h, l in CATER + BALE)
    return f'''<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div><h4>Finezja – sala bankietowa</h4><p>Kaczki Średnie 10c<br>62-700 Turek<br>NIP 7391718282</p>
<p><a href="tel:{TEL1H}">+48 {TEL1}</a><br><a href="tel:{TEL2H}">+48 {TEL2}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
<p><a href="{FB}" rel="noopener">Facebook</a> · <a href="{IG}" rel="noopener">Instagram</a> · <a href="{YT}" rel="noopener">YouTube</a></p></div>
<div><h4>Przyjęcia</h4><ul>{of}</ul></div>
<div><h4>Catering i bale</h4><ul>{ca}</ul></div>
<div><h4>Godziny otwarcia</h4><ul><li>Poniedziałek: 10:00–13:00</li><li>Czwartek: 9:00–13:00</li><li>Piątek–niedziela: 9:00–21:00</li></ul>
<h4 style="margin-top:26px">Finezja</h4><ul><li><a href="{p}galeria/">Galeria</a></li><li><a href="{p}polecamy/">Polecani wykonawcy</a></li><li><a href="{p}kontakt-2/">O nas</a></li><li><a href="{p}blog/">Blog</a></li><li><a href="{p}kontakt/">Kontakt</a></li></ul></div>
</div>
<div class="kpo">{pic(p, 'kpo', ALT['kpo'], '(max-width:700px) 100vw, 560px')}
<div><p><b>F.U. Finezja realizuje projekt dofinansowany ze środków Krajowego Planu Odbudowy.</b></p>
<p>W ramach inwestycji A1.2.1 Inwestycje dla przedsiębiorstw w produkty, usługi i kompetencje pracowników oraz kadry związane z dywersyfikacją działalności w ramach Krajowego Planu Odbudowy i Zwiększenia Odporności (planu rozwojowego).</p>
<p>„Dywersyfikacja usług FINEZJI poprzez zieloną transformację, zakup środków trwałych, cyfryzację oraz doradztwo i szkolenia w województwie wielkopolskim.”</p>
<p>Całkowita kwota wsparcia na realizację Przedsięwzięcia MŚP wynosi 485 235 zł.</p></div></div>
<div class="foot-mark" aria-hidden="true">Finezja</div>
<div class="foot-bottom"><span>© 2026 Finezja – sala bankietowa, Kaczki Średnie</span><span><a href="{p}polityka-prywatnosci/">Polityka prywatności</a></span></div>
</div>
</footer>
<div class="sticky-call"><a class="btn" href="tel:{TEL1H}">{ICO['tel']}Zadzwoń</a><a class="btn dark" href="{p}kontakt/#zapytanie">Zapytaj o termin</a></div>
<script src="{p}assets/lenis.min.js?v=1.1.20" defer></script>
<script src="{p}assets/app.js?v={V}" defer></script>
<script src="{p}assets/licznik.js" defer></script>
</body>
</html>
'''

def cta_band(p, h='Umów się na obejrzenie sali', t='Najlepiej zobaczyć Finezję na własne oczy. Zadzwoń lub napisz – pokażemy salę, plener, kuchnię i pokoje, a przy okazji opowiemy, czego nauczyło nas ponad 350 wesel.', mapa=False):
    m = f'<div class="map" data-lat="{LAT}" data-lng="{LNG}" role="img" aria-label="Mapa dojazdu do sali Finezja w Kaczkach Średnich"><div class="map-fallback">Kaczki Średnie 10c, 62-700 Turek</div></div>' if mapa else ''
    return f'''<section class="cta-band" id="kontakt">
<div class="wrap">
<div class="cta-grid">
<div><p class="over fade">Kaczki Średnie 10c · 4 km od Turku</p><h2 class="split">{h}</h2><p class="muted fade" style="max-width:52ch">{t}</p>
<a class="big-tel fade" href="tel:{TEL1H}"><span>{TEL1}</span></a>
<div class="acts fade" style="margin-top:0"><a class="btn" href="{p}kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn ghost" href="mailto:{MAIL}">{MAIL}</a></div></div>
<dl class="fade"><div><dt>Drugi telefon</dt><dd><a href="tel:{TEL2H}">{TEL2}</a></dd></div>
<div><dt>Adres</dt><dd><a href="{MAPS}" rel="noopener">Kaczki Średnie 10c, 62-700 Turek</a><br>Do Turku kilka minut, z Konina ok. 30 min, z Kalisza ok. 50 min</dd></div>
<div><dt>Godziny otwarcia</dt><dd>Pon. 10:00–13:00 · Czw. 9:00–13:00<br>Pt.–niedz. 9:00–21:00</dd></div></dl>
</div>
{m}
</div>
</section>
'''

def phead(p, img, crumbs, h1, lead='', over='', acts=True, short=False):
    cr = '<ol class="crumb fade"><li><a href="' + p + '">Strona główna</a></li>' + ''.join(
        f'<li><a href="{p}{h}">{l}</a></li>' if h else f'<li aria-current="page">{l}</li>' for h, l in crumbs) + '</ol>'
    ld = f'<p class="lead fade">{lead}</p>' if lead else ''
    ov = f'<p class="over fade">{over}</p>' if over else ''
    a = f'<div class="acts fade"><a class="btn" href="{p}kontakt/#zapytanie">Zapytaj o wolny termin</a><a class="btn ghost" href="tel:{TEL1H}">{ICO["tel"]}{TEL1}</a></div>' if acts else ''
    if not img:
        return f'<main id="tresc"><section class="phead text-only"><div class="wrap hero-in">{cr}{ov}<h1 class="split on-ready">{h1}</h1>{ld}{a}</div></section>'
    return f'''<main id="tresc"><section class="phead{' short' if short else ''}">
<div class="hero-media">{pic(p, img, ALT.get(img, ''), '100vw', lazy=False)}</div>
<div class="wrap hero-in">{cr}{ov}<h1 class="split on-ready">{h1}</h1>{ld}{a}</div>
</section>'''

def crumbs_ld(path, items):
    el = [{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": BASE}]
    for i, (h, l) in enumerate(items):
        el.append({"@type": "ListItem", "position": i + 2, "name": plain(l), "item": BASE + (h or path)})
    return {"@type": "BreadcrumbList", "itemListElement": el}

def faq_html(items, p):
    out = []
    for q, a in items:
        ans = ''.join(f'<p>{links(clean(x), p)}</p>' for x in a)
        out.append(f'<details><summary>{html.escape(q)}<i aria-hidden="true"></i></summary><div class="ans"><div>{ans}</div></div></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'

def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(' '.join(clean(x) for x in a))}} for q, a in items]}

PAGES = []
def write(path, doc):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(doc)
    PAGES.append(path)

# ---------------------------------------------------------------- renderer bloków z finezja.org
PRICE = re.compile(r'^(.*?)[\s:]*?(\d[\d\s]*(?:[.,]\d+)?\s*zł.*)$')

def menu_rows(lines):
    out = []
    for ln in lines:
        t = plain(ln)
        if ':' in t and re.search(r'\d\s*zł', t.split(':', 1)[1]): n, v = t.split(':', 1)
        else:
            m = PRICE.match(t)
            if not m: return None
            n, v = m.group(1), m.group(2)
        v = re.sub(r'(\d)\s*zł', r'\1 zł', v).replace('/1l', '/ 1 l').replace('/ 1l', '/ 1 l')
        out.append(f'<div class="mrow"><span class="n">{html.escape(n.strip(" –-"))}</span><span class="dots"></span><span class="v">{html.escape(v.strip())}</span></div>')
    return ''.join(out)

def is_price_line(t):
    t = plain(t); return len(t) < 75 and bool(re.search(r'\d\s*zł', t)) and (not t.endswith('.') or bool(re.search(r'(szt|kg|os)\.$', t)))

def head_like(b, nxt):
    if b['t'] != 'p' or nxt is None: return False
    x = b['x']; t = plain(x)
    if '<br>' in x or '<a ' in x or len(t) > 56 or len(t) < 3: return False
    if t[-1] in '.!:,;…' or re.search(r'\d\s*zł', t): return False
    if nxt['t'] == 'p' and head_like(nxt, {'t': 'p', 'x': 'x'}) and len(plain(nxt['x'])) < 30: return False
    return True

def only_links(x):
    t = plain(re.sub(r'<a [^>]*>(.*?)</a>', '', x))
    if x.count('<a ') == 1 and re.search(r'href="(tel|mailto):', x) and re.search(r'[@\d]', plain(x)): return False
    return '<a ' in x and not t

def btns(x, p, dark=False):
    out = []
    for i, (href, lab) in enumerate(re.findall(r'<a href="([^"]*)">(.*?)</a>', x)):
        cls = 'btn' if i == 0 else 'btn line'
        if dark and i: cls = 'btn ghost'
        out.append(f'<a class="{cls}" {links(f"href=\"{href}\"", p)}>{plain(lab)}</a>')
    return '<div class="inline-acts">' + ''.join(out) + '</div>'

def render_blocks(bl, p, ctx):
    """Bloki -> HTML (jedna sekcja). ctx: słownik strony (faq zbierane do JSON-LD)."""
    out = []; i = 0; prev_head = ''
    while i < len(bl):
        b = bl[i]; t = b['t']; nxt = bl[i + 1] if i + 1 < len(bl) else None
        if t in ('h2', 'h3', 'h4', 'h5', 'h6') or head_like(b, nxt):
            lvl = 'h2' if t == 'h2' else 'h3'
            x = clean(b['x']); x = re.sub(r'^<b>(.*)</b>$', r'\1', x)
            prev_head = plain(x)
            out.append(f'<{lvl}>{links(x, p)}</{lvl}>'); i += 1; continue
        if t == 'faq':
            items = []
            while i < len(bl) and bl[i]['t'] == 'faq':
                q = plain(clean(bl[i]['q'])); a = bl[i]['a']
                if plain(clean(a[0])) == q: q = 'Jaka jest minimalna wartość zamówienia?'
                items = [it for it in items if it[0] != q] + [(q, a)]; i += 1
            ctx['faq'] += items
            out.append(faq_html(items, p)); continue
        if t == 'img':
            fn = b['src'].rsplit('/', 1)[-1]; nm = RAWMAP.get(fn)
            if nm and nm not in ctx['used']:
                ctx['used'].add(nm)
                cls = 'ph poster' if nm in POSTER else 'ph'
                out.append(f'<figure class="{cls} fade">{pic(p, nm, ALT.get(nm, b["alt"]), "(max-width:700px) 100vw, 520px")}</figure>')
            i += 1; continue
        if t == 'btn':
            grp = []
            while i < len(bl) and bl[i]['t'] == 'btn':
                grp.append(f'<a href="{bl[i]["href"].replace("https://www.finezja.org", "")}">{bl[i]["x"]}</a>'); i += 1
            out.append(btns(' '.join(grp), p)); continue
        if t == 'table':
            rows = [[clean(c) for c in r] for r in b['rows']]
            ncol = max(len(r) for r in rows)
            hdr = len(rows) > 1 and (ncol > 2 and all(len(plain(c)) < 45 and '<a' not in c for c in rows[0]) or (ncol == 2 and plain(rows[0][1]) in ('Telefon', 'Co się dzieje', 'Jak to wygląda w praktyce')))
            if ncol == 2 and not hdr:
                out.append('<dl class="dl">' + ''.join(f'<dt>{links(re.sub(r"</?b>", "", r[0]), p)}</dt><dd>{links(r[1] if len(r) > 1 else "", p)}</dd>' for r in rows) + '</dl>')
            else:
                th = ''.join(f'<th scope="col">{c}</th>' for c in rows[0]) if hdr else ''
                body = rows[1:] if hdr else rows
                tb = ''.join('<tr>' + ''.join(f'<td>{links(c, p)}</td>' for c in r) + '</tr>' for r in body)
                out.append(f'<div class="tbl-wrap"><table>{"<thead><tr>" + th + "</tr></thead>" if th else ""}<tbody>{tb}</tbody></table></div>')
            i += 1; continue
        if t == 'ul':
            items = []
            for it in b['x']:
                it = clean(it)
                if len(re.findall(r'<b>[^<]{3,60}\.</b>', it)) > 1: items += [s for s in re.split(r'(?=<b>[^<]{3,60}\.</b>)', it) if plain(s)]
                else: items.append(it)
            mr = menu_rows(items) if all(is_price_line(x) for x in items) else None
            if mr: out.append(f'<div class="menu-list">{mr}</div>'); i += 1; continue
            ordered = bool(re.search(r'krok|^jak |zamówić|zarezerwować|działamy|ustalamy|współpraca', prev_head, re.I)) and not re.match(r'\d{1,2}[:.]\d{2}', plain(items[0]))
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag} class="ticks">' + ''.join(f'<li>{links(x, p)}</li>' for x in items) + f'</{tag}>'); i += 1; continue
        if t == 'p':
            x = clean(b['x'])
            if not plain(x): i += 1; continue
            if only_links(x): out.append(btns(x, p)); i += 1; continue
            if 'Kaczki Średnie 10c' in x and 'tel:' in x:
                out.append(f'<div class="contact-box"><p>{links(x, p)}</p></div>'); i += 1; continue
            lines = [l for l in x.split('<br>') if plain(l)]
            if len(lines) > 2 and all(is_price_line(l) for l in lines):
                rows = []
                while i < len(bl) and bl[i]['t'] == 'p':
                    ls = [l for l in clean(bl[i]['x']).split('<br>') if plain(l)]
                    if not all(is_price_line(l) for l in ls): break
                    rows += ls; i += 1
                out.append(f'<div class="menu-list">{menu_rows(rows)}</div>'); continue
            if re.match(r'^<b>[^<]{3,90}</b><br>', x):
                grp = []
                while i < len(bl) and bl[i]['t'] == 'p' and re.match(r'^<b>[^<]{3,90}</b><br>', clean(bl[i]['x'])):
                    y = clean(bl[i]['x']); hd, _, rest = y.partition('<br>')
                    grp.append(f'<div><h4>{plain(hd)}</h4><p>{links(rest, p)}</p></div>'); i += 1
                out.append(f'<div class="feats{" one" if len(grp) == 1 else ""}">' + ''.join(grp) + '</div>'); continue
            out.append(f'<p>{links(x, p)}</p>'); i += 1; continue
        i += 1
    return '\n'.join(out)

def sections(bl):
    secs = [[]]
    for b in bl:
        if b['t'] == 'h2' and secs[-1]: secs.append([])
        secs[-1].append(b)
    return [s for s in secs if s]

CTA_DROP = ('Umów się na obejrzenie sali', 'Zarezerwuj termin osiemnastki', 'Zarezerwuj termin wigilii firmowej', 'Zarezerwuj stolik na 21 listopada')

def page_body(path, bl, p, ctx, pool, intro_cls='paper'):
    """Sekcje strony: naprzemiennie tekst/zdjęcie, gdy jest zdjęcie z puli; ostatnią sekcję z kontaktem zastępuje pas kontaktowy."""
    out = []; k = 0
    secs = sections(bl)
    for si, s in enumerate(secs):
        h = plain(s[0]['x']) if s[0]['t'] == 'h2' else ''
        if h in CTA_DROP:
            ctx['band'] = (clean(s[0]['x']), plain(clean(s[1]['x'])) if len(s) > 1 and s[1]['t'] == 'p' else None); continue
        has_poster = any(b['t'] == 'img' and RAWMAP.get(b['src'].rsplit('/', 1)[-1]) in POSTER for b in s)
        inner = render_blocks(s, p, ctx)
        if not plain(re.sub(r'<figure.*?</figure>', '', inner, flags=re.S)) and '<figure' not in inner: continue
        bg = 'ivory' if si % 2 else 'paper'
        long_ = len(plain(inner)) > 500 or '<table' in inner or 'faq' in inner
        if pool and not has_poster and long_ and 'class="faq"' not in inner:
            img = pool[k % len(pool)]; k += 1
            flip = ' flip' if k % 2 == 0 else ''
            out.append(f'<section class="body-sec {bg}"><div class="wrap"><div class="row{flip}"><div class="txt prose fade">{inner}</div>'
                       f'<div class="media">{fig(p, img, ALT.get(img, ""))}</div></div></div></section>')
        else:
            out.append(f'<section class="body-sec {bg}"><div class="wrap narrow"><div class="prose fade">{inner}</div></div></section>')
    return '\n'.join(out)

def related(p, cur, items=OFERTA, h='Inne przyjęcia w Finezji'):
    li = ''.join(f'<li><a href="{p}{hh}">{l}</a></li>' for hh, l in items if hh != cur)
    return f'<section class="body-sec ivory"><div class="wrap"><h2 class="split" style="font-size:clamp(30px,3vw,44px)">{h}</h2><ul class="related fade">{li}</ul></div></section>'

# ---------------------------------------------------------------- podstrony z treści finezja.org
SUB = {
    # path: (hero, pula zdjęć, h1 (gdy brak w treści), nadtytuł, okruszki, opis SEO, powiązane)
    'wesele/': ('sala-kwiaty', ['stol-mlodych', 'dek-roze', 'slodki-stol', 'dek-luk', 'love', 'budynek-ogrod', 'dek-mlodzi', 'scena-dj'], None, 'Sala weselna · 60–160 gości', [(None, 'Wesele')],
                'Sala weselna 4 km od Turku dla 60–160 gości. Od 2010 roku ponad 350 wesel, menu 2026: 330–380 zł/os., własny alkohol bez korkowego, noclegi i plener.', OFERTA),
    'oferta/': ('urodziny-scianka', ['sala-stoly', 'chrzest-neon', 'stol-gosci', 'sala-okna'], 'Imprezy okolicznościowe w Finezji', 'Przyjęcia pod Turkiem', [(None, 'Przyjęcia')],
                'Urodziny, chrzciny, komunie, jubileusze, spotkania firmowe i konsolacje w sali bankietowej Finezja pod Turkiem.', OFERTA),
    'oferta/osiemnastka/': ('bal-parkiet', ['osiemnastka', 'scena-dj', 'slodki-babeczki', 'bal-scianka', 'dek-balony', 'stol-gosci'], None, 'Osiemnastka · do 150 gości', [('oferta/', 'Przyjęcia'), (None, 'Osiemnastka')],
                            'Sala na osiemnastkę w Turku i okolicach: sala na wyłączność, DJ, fotobudka 360, menu od 170 zł/os., zabawa do późna z dala od zabudowań.', OFERTA),
    'oferta/urodziny/': ('urodziny-scianka', ['urodziny-50', 'slodki-stol', 'stol-gosci'], None, 'Urodziny i jubileusze', [('oferta/', 'Przyjęcia'), (None, 'Urodziny')],
                         'Wynajem sali na urodziny, rocznice i jubileusze w Kaczkach Średnich pod Turkiem – kameralnie albo hucznie, z muzyką i tańcem.', OFERTA),
    'oferta/30-ste-urodziny/': ('bal-sala', ['urodziny-scianka', 'slodki-okno'], None, '30. urodziny', [('oferta/', 'Przyjęcia'), (None, '30. urodziny')],
                                'Sala na 30. urodziny pod Turkiem – rezerwacja na wyłączność, muzyka według Was i menu dopasowane do gości.', OFERTA),
    'oferta/czterdziestka/': ('dek-balony', ['sala-kwiaty', 'slodki-regal'], 'Restauracja na 40. urodziny', '40. urodziny', [('oferta/', 'Przyjęcia'), (None, '40. urodziny')],
                              'Restauracja na 40. urodziny pod Turkiem – kameralne przyjęcie albo uroczystość z rozmachem w sali Finezja.', OFERTA),
    'oferta/komunia-swieta/': ('stol-gosci', ['sala-okna', 'slodki-babeczki', 'nakrycie', 'kawa'], 'Komunia Święta w Finezji pod Turkiem', 'Komunia · 30–160 gości', [('oferta/', 'Przyjęcia'), (None, 'Komunia Święta')],
                               'Sala na komunię pod Turkiem: obiad serwowany, osobne menu dla dzieci, tort z własnej kuchni. 350 przyjęć komunijnych od 2010 roku.', OFERTA),
    'oferta/chrzest/': ('chrzest-neon', ['chrzest-pion', 'chrzest-balony', 'slodki-stol', 'stol-gosci', 'budynek-front'], 'Chrzciny w sali pod Turkiem', 'Chrzest Święty · 25–100 gości', [('oferta/', 'Przyjęcia'), (None, 'Chrzest Święty')],
                         'Chrzciny pod Turkiem: obiad od 90 zł/os., pakiet z ciastem od 110 zł/os., tort z własnej cukierni, ścianka „Chrzest Święty” w cenie.', OFERTA),
    'oferta/konsolacja/': ('sala-okna', ['stol-gosci'], 'Konsolacja – przyjęcie po pogrzebie', 'Konsolacja', [('oferta/', 'Przyjęcia'), (None, 'Konsolacja')],
                           'Konsolacja (stypa) w Finezji pod Turkiem – spokojna sala, proste menu i dyskretna obsługa, także z 2–3-dniowym wyprzedzeniem.', OFERTA),
    'oferta/spotkania-firmowe/': ('sala-dluga', ['sala-stoly', 'kawa'], 'Spotkania firmowe w restauracji', 'Dla firm', [('oferta/', 'Przyjęcia'), (None, 'Spotkania firmowe')],
                                  'Spotkania biznesowe, integracje i bankiety firmowe do 160 osób w restauracji Finezja pod Turkiem.', OFERTA),
    'catering-turek/': ('catering-bufet', ['slodki-stol', 'slodki-babeczki', 'kawa', 'slodki-regal'], None, 'Catering · od 5 do 100 osób', [(None, 'Catering Turek')],
                        'Catering z dowozem w Turku i okolicach: domowa kuchnia, konkretna cena za porcję, dowóz od kilku do 100 osób. Cennik dań, zup, ciast i tortów.', CATER),
    'wigilia/': ('stol-gosci', ['slodki-okno', 'kawa'], 'Wigilia w Restauracji Finezja – smaki tradycji', 'Catering wigilijny', [('catering-turek/', 'Catering'), (None, 'Catering wigilijny')],
                 'Catering wigilijny w okolicy Turku: barszcz z uszkami, pierogi, karp, kompot z suszu. Odbiór 23 grudnia w godz. 13:00–16:00.', CATER),
    'wigilia-firmowa/': ('sala-wieczor', ['sala-dluga', 'stol-gosci', 'slodki-regal'], 'Wigilia firmowa 2026 w Finezji', 'Dla firm · 20–160 osób', [('catering-turek/', 'Catering'), (None, 'Wigilia firmowa')],
                         'Wigilia firmowa pod Turkiem: sala na wyłączność albo catering do firmy. Zestawy od 149 zł/os., własny alkohol bez korkowego, faktura VAT.', CATER),
    'andrzejki/': ('bal-sala', ['bal-parkiet', 'scena-dj'], None, 'Sobota, 21 listopada 2026 · 19:00', [('andrzejki/', 'Bale'), (None, 'Bal Andrzejkowy 2026')],
                   'Bal Andrzejkowy 2026 w Turku – 21 listopada, start 19:00, bilety od 220 zł/os. Kolacja, DJ, zabawa do 4:00 w Sali Finezja.', BALE),
    'bal-noworoczny/': ('bal-parkiet', ['bal-sala'], 'Bal Noworoczny w Finezji', 'Bal Noworoczny', [('andrzejki/', 'Bale'), (None, 'Bal Noworoczny')],
                        'Bal Noworoczny w Sali Finezja pod Turkiem – posiłki, słodki stół, fotobudka 360, pokaz fajerwerków i zabawa do rana.', BALE),
    'karnawal/': ('bal-scianka', ['bal-parkiet'], 'Bal Karnawałowy w Finezji', 'Bal Karnawałowy', [('andrzejki/', 'Bale'), (None, 'Bal Karnawałowy')],
                  'Bal Karnawałowy w Sali Finezja pod Turkiem – kolacja, DJ i zabawa do rana.', BALE),
    'kontakt-2/': ('budynek-front', ['zespol', 'sala-zyrandole', 'budynek-wieczor'], 'Finezja. Sala, kuchnia i spokój – w jednym miejscu.', 'O nas', [(None, 'O nas')],
                   'Finezja to sala bankietowa pod Turkiem: wesela, komunie, chrzciny, urodziny, wigilie firmowe i catering. Sala na wyłączność, domowa kuchnia, własny alkohol bez korkowego.', None),
}
H1_FROM_FIRST = {'kontakt-2/'}

def sub_page(path):
    hero, pool, h1x, over, cr, desc, rel = SUB[path]
    v = T[path]; p = depth(path); bl = list(v['blocks'])
    if path == 'andrzejki/':      # na stronie wisi jeszcze opis balu z 2025 – zostaje tylko 2026
        j = next(i for i, b in enumerate(bl) if b['t'] == 'h1'); bl = bl[j:]
    if path in H1_FROM_FIRST and bl and bl[0]['t'] == 'img': bl = bl[1:]
    h1 = h1x
    if bl and bl[0]['t'] in ('h1',) or (path in H1_FROM_FIRST and bl[0]['t'] in ('h2', 'h3')):
        h1 = h1x or clean(bl[0]['x']); bl = bl[1:]
    elif bl and bl[0]['t'] == 'h2' and h1x is None:
        h1 = clean(bl[0]['x']); bl = bl[1:]
    elif h1 is None: h1 = v['title']
    if bl and bl[0]['t'] in ('h1',): bl = bl[1:]
    lead = ''
    if bl and bl[0]['t'] == 'p' and len(plain(bl[0]['x'])) < 420 and not only_links(bl[0]['x']) and not head_like(bl[0], bl[1] if len(bl) > 1 else None):
        lead = re.sub(r'</?b>', '', clean(bl[0]['x'])); bl = bl[1:]
    ctx = {'faq': [], 'used': set(), 'band': None}
    body = page_body(path, bl, p, ctx, pool)
    band = cta_band(p, *(x for x in ctx['band'] if x)) if ctx['band'] else cta_band(p)
    ld = [crumbs_ld(path, cr)] + ([faq_ld(ctx['faq'])] if ctx['faq'] else [])
    if path == 'andrzejki/':
        ld.append({"@type": "Event", "name": "Bal Andrzejkowy 2026 w Sali Finezja", "startDate": "2026-11-21T19:00:00+01:00", "endDate": "2026-11-22T04:00:00+01:00",
                   "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                   "location": {"@id": BASE + "#finezja"}, "image": BASE + 'img/' + IMG['plakat-andrzejki'][-1][2],
                   "offers": {"@type": "Offer", "price": "220", "priceCurrency": "PLN", "url": BASE + path}})
    title = plain(h1) if len(plain(h1)) < 60 else v['title']
    doc = (head(p, path, f'{title} – Finezja, sala bankietowa pod Turkiem', desc, ld, preload=big(p, hero), og=hero) + header(p, path)
           + phead(p, hero, cr, h1, lead, over) + body
           + (related(p, path, rel, 'Zobacz też') if rel else '') + band + '</main>' + footer(p))
    write(path, doc)

# ---------------------------------------------------------------- strona główna
REVIEWS = [
    ('Dominika Kawia', 'Organizowałam tu wesele syna, ponieważ urzekł mnie klimat tego miejsca i fantastyczna obsługa. Jednakże największym potwierdzeniem doskonałego wyboru były zachwyty gości nad podanymi daniami. Fakt – były niesamowite.', 'wesele'),
    ('Jolanta G', 'Wesele w Finezji było dla nas niezapomnianym przeżyciem. Sala była pięknie oświetlona, a aranżacje kwiatowe dodawały uroku całemu miejscu. Jedzenie było po prostu przepyszne, szczególnie tarta tatarska i szaszłyki.', 'wesele'),
    ('Nina Kokoszko', 'Wyrażam pozytywną opinię z 18 mojej córki, która odbyła się w miniony piątek w restauracji Finezja. Jedzenie było przepyszne, świeże, a Panie w obsłudze i kuchni przemiłe. To nie była moja pierwsza impreza, lecz kolejna na tej sali, i nic mnie nie zawiodło.', 'osiemnastka'),
    ('Wioletta Wędzik', 'Robiliśmy u Państwa niejedną imprezę i jak zawsze jesteśmy bardzo zadowoleni. Jedzenie przepyszne, dużo i te wasze devolaje, obsługa na najwyższym poziomie, przemili ludzie. Z cateringu również jesteśmy zadowoleni – przede wszystkim ciepły.', 'przyjęcia i catering'),
    ('Andrej Kurawa', 'Zamówiony udziec z dodatkami dla 20 osób plus kilka sałatek na zimno – pierwsza klasa, wykonanie bardzo smaczne, każdy gość bardzo zadowolony. Na pewno jeszcze powtórzę zamówienie.', 'catering'),
    ('Małgorzata Gaj', 'Bardzo fajne miejsce na imprezę. Jedzonko wyśmienite, obsługa bardzo miła. Polecam na większe i mniejsze uroczystości rodzinne.', 'przyjęcie rodzinne'),
    ('marcin tomek', 'Catering na czas, wszystko ciepłe i pyszne – polecam!', 'catering'),
]

def home():
    p = ''; v = T['']; bl = v['blocks']
    faq = [(plain(clean(b['q'])), b['a']) for b in bl if b['t'] == 'faq']
    spec_rows = next(b for b in bl if b['t'] == 'table')['rows']
    spec = {plain(r[0]): clean(r[1]) for r in spec_rows}
    grp = [('sala-zyrandole', ['Doświadczenie', 'Pojemność sali', 'Wnętrze']), ('scena-dj', ['Układy stołów', 'Parkiet']),
           ('slodki-stol', ['Kuchnia', 'Tort i desery']), ('bal-parkiet', ['Atrakcje na miejscu', 'Parking', 'Zabawa', 'Hałas']),
           ('love', ['Plener']), ('budynek-ogrod', ['Noclegi'])]
    sm = ''.join(f'<img src="img/{next(x for x in IMG[g] if x[0] >= 1100)[2] if any(x[0] >= 1100 for x in IMG[g]) else IMG[g][-1][2]}" alt="{html.escape(ALT[g])}" loading="lazy" decoding="async"{" class=\"on\"" if i == 0 else ""}>' for i, (g, _) in enumerate(grp))
    sg = ''.join(f'<div class="spec-grp" data-i="{i}"><figure class="ph m-ph">{pic(p, g, ALT[g], "100vw")}</figure><dl class="spec-list">'
                 + ''.join(f'<div class="spec-row"><dt>{k}</dt><dd>{spec[k]}</dd></div>' for k in ks) + '</dl></div>' for i, (g, ks) in enumerate(grp))
    occ = [('wesele/', 'Wesela', 'Ponad 350 wesel od 2010 roku. 60–160 gości, jedno wesele dziennie, zabawa do rana, ok. 48 noclegów w Kaczkach Średnich.', '330–380 zł/os.', 'menu 2026', 'stol-mlodych'),
           ('oferta/osiemnastka/', 'Osiemnastki', '730 osiemnastek – najczęstsza impreza w Finezji. 40–160 osób, nagłośnienie, fotobudka i kamera 360, obsługa od początku do końca.', 'od 170 zł/os.', '', 'osiemnastka'),
           ('oferta/komunia-swieta/', 'Komunie', '350 przyjęć komunijnych. Obiad serwowany z ciastami i kawą, osobne menu dla dzieci, tort komunijny z własnej kuchni.', '200 zł/os.', '', 'nakrycie'),
           ('oferta/chrzest/', 'Chrzciny', '390 przyjęć chrzcinowych. Kameralnie w części sali, kącik dla dzieci, ścianka „Chrzest Święty” w cenie.', 'od 90 zł/os.', 'z ciastem od 110 zł', 'chrzest-pion'),
           ('oferta/urodziny/', 'Urodziny i jubileusze', '30-tki, 40-tki, 50-tki, rocznice ślubu – kameralnie albo hucznie, z parkietem i DJ-em.', '', '', 'urodziny-scianka'),
           ('wigilia-firmowa/', 'Imprezy firmowe i wigilie', 'Spotkania i wigilie pracownicze do 160 osób – w sali albo z cateringiem do firmy. Faktura VAT.', 'od 149 zł/os.', 'wigilia firmowa', 'sala-dluga'),
           ('oferta/konsolacja/', 'Konsolacje', 'Przyjęcia po pogrzebie nawet z 2–3-dniowym wyprzedzeniem, z prostym menu i dyskretną obsługą.', 'od 65 zł/os.', '', 'sala-okna'),
           ('catering-turek/', 'Catering i święta', 'Dania z dowozem dla 5–100 osób, potrawy wigilijne i wielkanocne na wynos. Turek i okolice do 40 km.', 'cena za porcję', '', 'catering-bufet')]
    occ_li = ''.join(f'<li><a href="{h}"><span class="th">{pic(p, im, ALT[im], "96px")}</span><h3>{n}</h3><p>{d}</p><span class="pr">{pr}{f"<small>{sm_}</small>" if sm_ else ""}</span></a></li>'
                     for h, n, d, pr, sm_, im in occ)
    float_imgs = ''.join(f'<img src="img/{IMG[im][0][2] if IMG[im][0][0] >= 600 else IMG[im][-1][2]}" alt="" loading="lazy">' for *_, im in occ)
    why = [('16 sezonów, ponad 2000 przyjęć', 'Wiemy, kiedy podać tort, żeby nie kolidował z blokiem tanecznym, jak rozsadzić rodziny i jak poprowadzić osiemnastkę tak, żeby rodzice byli spokojni, a jubilat zadowolony.'),
           ('Jedno przyjęcie dziennie', 'Sala, kuchnia i obsługa pracują wyłącznie dla Was. Nie dzielicie parkingu ani parkietu z inną imprezą.'),
           ('Wszystko w jednym miejscu', 'Własna kuchnia i torty, fotobudka i kamera 360, noclegi, plener, koordynator – plus 17 sprawdzonych partnerów: DJ-e, floryści, fotografowie, animator, barman, cukiernia.'),
           ('Bez ukrytych kosztów', 'Własny alkohol bez opłaty korkowej, własna ekipa (DJ, fotograf, dekorator) bez dodatkowych opłat, dekoracja stołów i koordynator w cenie menu.'),
           ('4 km od Turku, cisza dookoła', 'Do centrum Turku kilka minut, do Konina ok. 30 min, do Kalisza ok. 45 min. Zabudowań w pobliżu brak, więc muzyka gra do rana.'),
           ('Ocena 4,6 z 340 opinii Google', 'Najczęściej chwalone: jedzenie („tarta tatarska”, „szaszłyki”, „de volaille”), obsługa i klimat sali. Odpowiadamy na każdą opinię, także krytyczną.')]
    revs = ''.join(f'<figure class="rev"><blockquote>„{t}”</blockquote><figcaption><b>{n}</b><span>{k} · Google</span></figcaption></figure>' for n, t, k in REVIEWS)
    posts = ''.join(post_card(p, k) for k in POSTS[:3])
    local = [(b['x'], bl[i + 1]['x']) for i, b in enumerate(bl) if b['t'] == 'h3' and i + 1 < len(bl) and bl[i + 1]['t'] == 'p' and
             plain(b['x']) in ('Rodzinne i firmowe imprezy — Turek i okolice', 'Organizacja imprez z jedzeniem w pobliżu Turku', 'Szukasz sali bankietowej? Wybierz Finezję!', 'Dlaczego sala bankietowa Finezja to najlepszy wybór?')]
    local_html = ''.join(f'<div class="fade"><h3>{plain(clean(h))}</h3><p>{links(clean(t), p)}</p></div>' for h, t in local)
    desc = 'Sala bankietowa i weselna Finezja 4 km od Turku: 60–160 gości, własna kuchnia, noclegi, plener i zabawa do rana. Wesela, osiemnastki, komunie, chrzciny, catering. Od 2010 roku.'
    doc = head(p, '', 'Sala bankietowa Finezja w Turku – wesela, przyjęcia, catering', desc, [faq_ld(faq)], preload=f'img/{IMG["wieczor"][-1][2]}', og='wieczor') + header(p, '') + f'''<main id="tresc">
<section class="hero">
<div class="hero-media"><video data-auto autoplay muted loop playsinline preload="auto" poster="img/{IMG['wieczor'][-1][2]}" aria-hidden="true"><source src="media/wieczor.mp4" type="video/mp4"></video></div>
<div class="wrap hero-in">
<p class="over fade">Kaczki Średnie · 4 km od Turku · od 2010 roku</p>
<h1 class="split on-ready" data-delay=".1">Sala bankietowa Finezja w Turku</h1>
<p class="lead fade">Miejsce na Twoje wymarzone przyjęcie – wesele, osiemnastkę, komunię, chrzciny albo spotkanie firmowe. Sala dla 60–160 gości z własną kuchnią, noclegami i ciszą dookoła.</p>
<div class="acts fade"><a class="btn" href="kontakt/#zapytanie">Sprawdź wolny termin</a><a class="btn ghost" href="tel:{TEL1H}">{ICO['tel']}{TEL1}</a></div>
<div class="hero-foot fade"><a href="{GOOGLE}" rel="noopener"><span class="star">★★★★★</span> 4,6 · 340 opinii w Google</a><span>ponad 2000 przyjęć</span><span>jedno przyjęcie dziennie</span><span>bezpłatny parking</span></div>
</div>
<div class="hero-cue" aria-hidden="true"></div>
</section>

<section class="paper">
<div class="wrap">
<div class="intro-grid">
<h2 class="split">Nowoczesność, klasyczna elegancja i spokój natury</h2>
<div class="txt fade"><p class="lead">Organizacja ważnych uroczystości – wesela, urodzin, komunii czy spotkania firmowego – wymaga odpowiedniej oprawy i atmosfery. Dlatego warto wybrać miejsce, które spełni <b>wszystkie oczekiwania, zarówno pod względem estetycznym, jak i organizacyjnym</b>.</p>
<p class="muted">Sala bankietowa Finezja łączy nowoczesność z klasyczną elegancją. Położona w malowniczej okolicy, zaledwie 4 kilometry od Turku, oferuje nie tylko <b>piękne wnętrza, ale również spokój i bliskość natury</b>. Goście łatwo dojadą na przyjęcie, a na miejscu mają ciszę z dala od miejskiego zgiełku.</p></div>
</div>
<div class="wide-ph">{fig(p, 'sala-nowa', ALT['sala-nowa'], sizes='100vw')}</div>
</div>
</section>

<section class="ivory">
<div class="wrap">
<div class="count-head"><div><p class="over fade">Ile było wydarzeń?</p><h2 class="split">Elegancka i przestronna sala bankietowa</h2>
<p class="muted fade" style="max-width:60ch">Sala i restauracja na <b>60–160 gości</b> z własną kuchnią, bezpłatnym parkingiem, plenerem i noclegami. Przyjeżdżają do nas rodziny i firmy z Turku, Konina, Koła, Kalisza, Dobrej, Władysławowa i Uniejowa.</p></div>
<p class="total fade">od 2010 roku<b><span data-count="2000">2000</span>+</b>przyjęć</p></div>
<div class="ledger fade"><div><b data-count="350">350</b><span>wesel</span></div><div><b data-count="730">730</b><span>osiemnastek</span></div><div><b data-count="390">390</b><span>chrzcin</span></div><div><b data-count="350">350</b><span>komunii</span></div><div><b data-count="200">200</b><span>jubileuszy, konsolacji i imprez firmowych</span></div></div>
</div>
</section>

<section class="night">
<div class="wrap">
<div class="sec-head"><div><p class="over fade">Sala Finezja w szczegółach</p><h2 class="split">Jak wygląda sala?</h2></div><p class="fade">Jasne, wysokie wnętrze bez narzuconych dekoracji – tło, które dopasujemy do Waszego przyjęcia.</p></div>
<div class="spec">
<div class="spec-media" aria-hidden="true">{sm}<span class="cap">{ALT[grp[0][0]]}</span></div>
<div>{sg}
<div class="acts fade"><a class="btn" href="mailto:{MAIL}">Zarezerwuj termin</a><a class="btn ghost" href="tel:{TEL1H}">Zadzwoń: {TEL1}</a></div></div>
</div>
</div>
</section>

<section class="paper">
<div class="wrap">
<div class="sec-head"><div><p class="over fade">Finezja sala bankietowa · Turek</p><h2 class="split">Jakie przyjęcia organizujemy w Finezji?</h2></div>
<p class="fade">Niezależnie od rodzaju przyjęcia nasz zespół pomaga na każdym etapie – od wyboru menu, przez dekoracje, po obsługę techniczną.</p></div>
<ul class="occ fade">{occ_li}</ul>
<div class="float-ph" aria-hidden="true">{float_imgs}</div>
</div>
</section>

<section class="ivory">
<div class="wrap">
<div class="kitchen">
<div class="stack">{fig(p, 'slodki-babeczki', ALT['slodki-babeczki'])}<figure class="ph b reveal" data-par="-.06">{pic(p, 'kawa', ALT['kawa'], '(max-width:1000px) 50vw, 25vw')}</figure></div>
<div>
<p class="over fade">Wykwintna kuchnia – Finezja smaku</p>
<h2 class="split">Własna kuchnia, własne torty</h2>
<div class="fade"><p>Wszystkie dania gotujemy na miejscu – <b>nie korzystamy z cateringu z zewnątrz</b>. Menu układamy z każdym klientem osobno: klasyczna kuchnia polska dla starszych gości (rosół, pieczenie, de volaille – wielokrotnie chwalone w opiniach), nowoczesne propozycje dla młodszych, pełnowartościowe dania wegetariańskie, wegańskie, bezglutenowe i bez laktozy.</p>
<p class="muted"><b>Tort i słodki stół robimy sami.</b> Nasza cukiernia przygotowuje torty na śmietanie, torty lodowe, deserki i monoporcje. Tort nie jedzie w upale – trafia na stół prosto z kuchni.</p></div>
<div class="menu-card fade"><h3>Ceny orientacyjne (2026)</h3>
<div class="mrow"><span class="n">Menu weselne</span><span class="dots"></span><span class="v">330–380 zł/os.</span></div>
<div class="mrow"><span class="n">Osiemnastka</span><span class="dots"></span><span class="v">170 zł/os.</span></div>
<div class="mrow"><span class="n">Komunia</span><span class="dots"></span><span class="v">200 zł/os.</span></div>
<div class="mrow"><span class="n">Chrzciny – obiad / z ciastem</span><span class="dots"></span><span class="v">od 90 / 110 zł/os.</span></div>
<div class="mrow"><span class="n">Obiad okolicznościowy, konsolacja</span><span class="dots"></span><span class="v">od 65 zł/os.</span></div>
<div class="mrow"><span class="n">Catering na wynos</span><span class="dots"></span><span class="v">wycena indywidualna</span></div>
<p class="small muted" style="margin:14px 0 0">Napoje bezalkoholowe bez limitu, <b>alkohol przywozicie własny – bez opłaty korkowej.</b> Przed weselem zapraszamy na degustację.</p></div>
<div class="acts fade"><a class="btn dark" href="mailto:{MAIL}?subject=Wesele%20-%20menu">Zapytaj o menu mailem</a><a class="btn line" href="tel:{TEL1H}">Umów wizytę w sali</a></div>
</div>
</div>
</div>
</section>

<section class="freeze">
<div class="bg">{pic(p, 'stol-mlodych', ALT['stol-mlodych'], '100vw')}</div>
<div class="wrap"><blockquote class="split">Jedno przyjęcie dziennie.</blockquote><p class="fade">Sala, kuchnia i obsługa pracują wyłącznie dla Was. Nie dzielicie parkingu, kuchni ani parkietu z inną imprezą – a sala stoi z dala od zabudowań, więc zabawa trwa do rana.</p></div>
</section>

<section class="paper">
<div class="wrap">
<div class="why">
<div class="ph-side"><p class="over fade">Profesjonalna obsługa na najwyższym poziomie</p><h2 class="split">Dlaczego klienci wybierają Finezję?</h2>
{fig(p, 'zespol', ALT['zespol'], cap='Zespół Finezji – kuchnia i obsługa')}</div>
<div class="why-list">{''.join(f'<div class="fade"><h3>{h}</h3><p>{t}</p></div>' for h, t in why)}</div>
</div>
</div>
</section>

<section class="night">
<div class="wrap">
<div class="sec-head"><div><p class="over fade">Współpraca z nami</p><h2 class="split">Robimy to co tydzień. Wy robicie to raz.</h2></div><p class="fade">Od pierwszego telefonu do ostatniego tańca – tak wygląda przygotowanie przyjęcia w Finezji.</p></div>
<ol class="steps"><span class="bar" aria-hidden="true"></span>
<li class="fade"><span class="k">Krok 1</span><h3>Rozmowa</h3><p>Mówicie, na kiedy i na ile osób planujecie wydarzenie. Doradzimy, co się sprawdzi – najlepiej na miejscu, w sali.</p></li>
<li class="fade"><span class="k">Krok 2</span><h3>Termin i menu</h3><p>Ustalamy datę, liczbę gości i menu. Wszystko na piśmie, bez domysłów.</p></li>
<li class="fade"><span class="k">Krok 3</span><h3>Szczegóły</h3><p>Dekoracja, harmonogram dnia, dodatki – ustalamy z wyprzedzeniem, żeby w dniu imprezy nie było niespodzianek.</p></li>
<li class="fade"><span class="k">Krok 4</span><h3>Dzień wydarzenia</h3><p>Sala gotowa, stół nakryty, kuchnia i obsługa na miejscu. Wy tylko witacie gości.</p></li>
</ol>
</div>
</section>

<section class="ivory">
<div class="wrap">
<div class="rev-head"><div><p class="over fade">Co mówią nasi Goście</p><h2 class="split" style="margin:0">Opinie z Google</h2></div>
<a class="rating fade" href="{GOOGLE}" rel="noopener"><b>4,6</b><span><span class="stars">★★★★★</span><br>340 opinii w Google</span></a>
<div class="rev-nav fade"><button type="button" data-track="rt" data-dir="prev" aria-label="Poprzednia opinia">{ICO['prev']}</button><button type="button" data-track="rt" data-dir="next" aria-label="Następna opinia">{ICO['next']}</button></div></div>
<div class="rev-track" id="rt">{revs}</div>
</div>
</section>

<section class="night-2">
<div class="wrap">
<div class="sec-head"><div><p class="over fade">Najbliższe wydarzenia</p><h2 class="split">Jesień i grudzień w Finezji</h2></div><p class="fade">Bal Andrzejkowy otwarty dla wszystkich i wigilie firmowe – soboty grudnia rozchodzą się zwykle już w październiku.</p></div>
<div class="events">
<a class="ev fade" href="andrzejki/"><figure class="ph">{pic(p, 'plakat-andrzejki', ALT['plakat-andrzejki'], '(max-width:700px) 100vw, 260px')}</figure><div><p class="when">Sobota, 21 listopada 2026 · 19:00</p><h3>Bal Andrzejkowy 2026</h3><p>Uroczysta kolacja, żurek, kulinarna niespodzianka, druga ciepła kolacja po północy i DJ do 4:00. Bilety od 220 zł/os.</p><span class="u">Program i rezerwacja</span></div></a>
<a class="ev fade" href="wigilia-firmowa/"><figure class="ph">{pic(p, 'menu-wigilia-firmowa', ALT['menu-wigilia-firmowa'], '(max-width:700px) 100vw, 260px')}</figure><div><p class="when">Grudzień 2026 · 20–160 osób</p><h3>Wigilia firmowa</h3><p>Sala na wyłączność albo catering do firmy. Trzy zestawy: Tradycyjny 149 zł, Świąteczny 179 zł i Bankietowy 209 zł od osoby.</p><span class="u">Menu i kosztorys</span></div></a>
</div>
</div>
</section>

<section class="paper" id="faq">
<div class="wrap">
<div class="faq-grid">
<div class="side"><p class="over fade">FAQ</p><h2 class="split">Najczęściej zadawane pytania</h2><p class="muted fade">Nie ma tu Twojego pytania? Zadzwoń – odpowiemy od ręki.</p>
<div class="acts fade"><a class="btn dark" href="tel:{TEL1H}">{ICO['tel']}{TEL1}</a></div></div>
{faq_html(faq, p)}
</div>
</div>
</section>

<section class="ivory">
<div class="wrap">
<div class="sec-head"><div><p class="over fade">Aktualności</p><h2 class="split">Blog</h2></div><a class="u fade" href="blog/">Wszystkie wpisy</a></div>
<div class="posts">{posts}</div>
</div>
</section>

<section class="paper">
<div class="wrap"><div class="local">{local_html}</div></div>
</section>
''' + cta_band(p, 'Zarezerwuj swoje przyjęcie w Finezji', 'Planujesz wesele, urodziny, komunię czy spotkanie firmowe? Skontaktuj się z nami i zarezerwuj termin – sala bankietowa Finezja pod Turkiem czeka na Twoją uroczystość.', mapa=True) + '</main>' + footer(p)
    write('', doc)

# ---------------------------------------------------------------- blog
POSTIMG = {'catering': 'catering-bufet', 'wigilia': 'stol-gosci', 'wesel': 'dek-roze', 'osiemnastk': 'osiemnastka', 'komuni': 'nakrycie', 'chrzest': 'chrzest-neon',
           'konsolacja': 'sala-okna', '18-lat': 'bal-parkiet', 'swiateczny': 'slodki-okno', 'plenerze': 'love', 'menu': 'slodki-babeczki', 'obsluga': 'kawa', 'sprawdzic': 'sala-zyrandole'}
def post_img(k):
    for key in ('plenerze', 'swiateczny', 'sprawdzic', 'obsluga', 'menu', 'osiemnastk', '18-lat', 'wigilia', 'catering', 'wesel', 'komuni', 'chrzest', 'konsolacja'):
        if key in k: return POSTIMG[key]
    return 'sala-kwiaty'

MIES = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
def pl_date(s): y, m, d = s.split('-'); return f'{int(d)} {MIES[int(m) - 1]} {y}'

def post_card(p, k):
    v = T[k]; im = post_img(k)
    return f'<a class="post fade" href="{p}{k}"><figure class="ph">{pic(p, im, ALT[im], "(max-width:700px) 100vw, 33vw")}</figure><time datetime="{v["date"]}">{pl_date(v["date"])}</time><h3>{html.escape(v["title"])}</h3></a>'

def blog():
    p = '../'
    cards = ''.join(post_card(p, k) for k in POSTS)
    doc = (head(p, 'blog/', 'Blog – Finezja, sala bankietowa pod Turkiem', 'Porady o organizacji wesel, osiemnastek, chrzcin, komunii, wigilii firmowych i cateringu od zespołu sali Finezja pod Turkiem.', [crumbs_ld('blog/', [(None, 'Blog')])])
           + header(p, 'blog/') + phead(p, None, [(None, 'Blog')], 'Blog Finezji', 'Organizacja wesel, osiemnastek, chrzcin i wigilii firmowych – z doświadczenia ponad 2000 przyjęć.', 'Aktualności', acts=False)
           + f'<section class="paper"><div class="wrap"><div class="posts">{cards}</div></div></section>' + cta_band(p) + '</main>' + footer(p))
    write('blog/', doc)

def post(k):
    v = T[k]; p = depth(k); bl = list(v['blocks'])
    if bl and bl[0]['t'] == 'h1': bl = bl[1:]
    ctx = {'faq': [], 'used': set(), 'band': None}
    im = post_img(k)
    cat = CATNAME.get((v['cats'] or [1])[0], 'Blog')
    inner = render_blocks(bl, p, ctx)
    ld = [crumbs_ld(k, [('blog/', 'Blog'), (None, v['title'])]),
          {"@type": "BlogPosting", "headline": v['title'], "datePublished": v['date'], "dateModified": v['modified'], "author": {"@id": BASE + "#finezja"},
           "publisher": {"@id": BASE + "#finezja"}, "image": BASE + 'img/' + IMG[im][-1][2], "mainEntityOfPage": BASE + k}] + ([faq_ld(ctx['faq'])] if ctx['faq'] else [])
    desc = (v['yoast'] or {}).get('description') or plain(v['excerpt'])[:155]
    rel = ''.join(post_card(p, x) for x in [x for x in POSTS if x != k][:3])
    doc = (head(p, k, f'{v["title"]} – Finezja', desc, ld, og=im) + header(p, 'blog/')
           + phead(p, None, [('blog/', 'Blog'), (None, cat)], html.escape(v['title']), '', f'{cat} · {pl_date(v["date"])}', acts=False)
           + f'<section class="paper"><div class="wrap"><div class="post-body"><figure class="ph reveal">{pic(p, im, ALT[im], "(max-width:800px) 100vw, 740px")}</figure><div class="prose fade">{inner}</div></div></div></section>'
           + f'<section class="ivory"><div class="wrap"><div class="sec-head"><h2 class="split" style="font-size:clamp(30px,3vw,44px)">Przeczytaj też</h2><a class="u" href="{p}blog/">Wszystkie wpisy</a></div><div class="posts">{rel}</div></div></section>'
           + cta_band(p) + '</main>' + footer(p))
    write(k, doc)

# ---------------------------------------------------------------- galeria
GAL = [('sala', ['sala-nowa', 'hero', 'sala-zyrandole', 'sala-kwiaty', 'sala-dluga', 'sala-okna', 'sala-stoly', 'sala-pion', 'sala-okragle', 'sala-wieczor', 'nakrycie', 'stol-gosci', 'scena-dj']),
       ('dekoracje', ['stol-mlodych', 'dek-roze', 'dek-kwiaty', 'dek-luk', 'dek-mlodzi', 'dek-oltarz', 'dek-milosc', 'dek-stol']),
       ('slodki', ['slodki-stol', 'slodki-babeczki', 'slodki-okno', 'slodki-regal', 'kawa', 'catering-bufet']),
       ('okazje', ['osiemnastka', 'urodziny-scianka', 'urodziny-50', 'urodziny-pion', 'chrzest-neon', 'chrzest-pion', 'chrzest-balony', 'scianka-mis', 'dek-balony', 'bal-sala', 'bal-parkiet', 'bal-scianka']),
       ('budynek', ['budynek-front', 'budynek-ogrod', 'budynek-plac', 'budynek-wieczor', 'budynek-dzien', 'wejscie', 'love', 'wieczor'])]
GALN = {'sala': 'Sala', 'dekoracje': 'Dekoracje', 'slodki': 'Słodki stół i kuchnia', 'okazje': 'Urodziny, chrzciny, bale', 'budynek': 'Budynek i plener'}

def galeria():
    p = '../'; v = T['galeria/']; bl = v['blocks']
    items = ''.join(f'<a href="{big(p, n)}" data-full="{big(p, n)}" data-c="{c}" data-nodoor>{pic(p, n, ALT[n], "(max-width:700px) 100vw, (max-width:1000px) 50vw, 33vw")}</a>' for c, ns in GAL for n in ns)
    flt = '<button type="button" data-f="*" aria-pressed="true">Wszystkie</button>' + ''.join(f'<button type="button" data-f="{c}" aria-pressed="false">{GALN[c]}</button>' for c, _ in GAL)
    tail = [b for b in bl if b['t'] in ('h2', 'p')][2:]
    ctx = {'faq': [], 'used': set(), 'band': None}
    doc = (head(p, 'galeria/', 'Galeria – sala bankietowa Finezja pod Turkiem', 'Zdjęcia sali Finezja: wnętrze z lustrzanym sufitem, dekoracje weselne, słodkie stoły, osiemnastki, chrzciny i budynek z ogrodem w Kaczkach Średnich.', [crumbs_ld('galeria/', [(None, 'Galeria')])], og='sala-zyrandole')
           + header(p, 'galeria/') + phead(p, 'sala-zyrandole', [(None, 'Galeria')], 'Jak zmieniła się nasza sala', 'Na przestrzeni ostatnich lat nasz lokal się zmienił. Tak dziś wyglądają sala, dekoracje i przyjęcia w Finezji.', 'Galeria', short=True)
           + f'<section class="paper"><div class="wrap"><div class="gal-filter fade" role="group" aria-label="Filtr zdjęć">{flt}</div><div class="gal">{items}</div></div></section>'
           + f'<section class="ivory body-sec"><div class="wrap narrow"><div class="prose fade">{render_blocks(tail, p, ctx)}</div></div></section>'
           + f'<div class="lb" role="dialog" aria-modal="true" aria-label="Podgląd zdjęcia"><img alt=""><button class="x" type="button" aria-label="Zamknij">{ICO["x"]}</button><button class="pv" type="button" aria-label="Poprzednie">{ICO["prev"]}</button><button class="nx" type="button" aria-label="Następne">{ICO["next"]}</button><div class="cnt"></div></div>'
           + cta_band(p) + '</main>' + footer(p))
    write('galeria/', doc)

# ---------------------------------------------------------------- polecamy
def polecamy():
    p = '../'; bl = T['polecamy/']['blocks']
    secs = []; cur = None
    for b in bl:
        if b['t'] == 'h2': cur = [plain(b['x']), []]; secs.append(cur)
        elif b['t'] == 'p' and cur and 'tel:' in b['x']:
            cur[1][-1][1] = re.search(r'href="tel:([^"]+)">([^<]+)', b['x']).groups()
        elif b['t'] == 'p' and cur: cur[1].append([plain(b['x']), None])
    imgs = ['scena-dj', 'bal-parkiet', 'dek-luk', 'love']
    rows = []
    for i, (h, ppl) in enumerate(secs):
        tb = ''.join(f'<tr><td>{html.escape(n)}</td><td><a href="tel:{t[0]}">{t[1].replace("+48 ", "")}</a></td></tr>' for n, t in ppl if t)
        rows.append(f'<section class="body-sec {"ivory" if i % 2 else "paper"}"><div class="wrap"><div class="row{" flip" if i % 2 else ""}"><div class="txt prose fade"><h2>{h}</h2>'
                    f'<div class="tbl-wrap"><table><thead><tr><th>Wykonawca</th><th>Telefon</th></tr></thead><tbody>{tb}</tbody></table></div></div>'
                    f'<div class="media">{fig(p, imgs[i % 4], ALT[imgs[i % 4]])}</div></div></div></section>')
    doc = (head(p, 'polecamy/', 'Polecani wykonawcy – zespoły, DJ-e, dekoratorzy, fotografowie | Finezja', 'Sprawdzeni lokalni wykonawcy, którzy znają salę Finezja: zespoły i DJ-e na wesele, dekoratorzy i fotografowie z okolic Turku.', [crumbs_ld('polecamy/', [(None, 'Polecamy')])], og='scena-dj')
           + header(p, 'polecamy/') + phead(p, 'scena-dj', [(None, 'Polecamy')], 'Polecani wykonawcy', 'Poniżej przedstawiamy naszych lokalnych wykonawców. To sprawdzone osoby, które znają salę i nasz harmonogram.', 'Polecamy', short=True)
           + ''.join(rows) + cta_band(p) + '</main>' + footer(p))
    write('polecamy/', doc)

# ---------------------------------------------------------------- kontakt
def kontakt():
    p = '../'
    form = f'''<form class="form fade" id="zapytanie" action="mailto:{MAIL}" method="post" enctype="text/plain">
<label>Imię i nazwisko<input name="imie" autocomplete="name" required></label>
<label>Telefon<input name="tel" type="tel" autocomplete="tel" required></label>
<label>E-mail<input name="email" type="email" autocomplete="email"></label>
<label>Rodzaj przyjęcia<select name="rodzaj"><option>Wesele</option><option>Osiemnastka</option><option>Urodziny / jubileusz</option><option>Komunia</option><option>Chrzciny</option><option>Wigilia firmowa</option><option>Spotkanie firmowe</option><option>Konsolacja</option><option>Catering</option><option>Bal Andrzejkowy 2026</option><option>Inne</option></select></label>
<label>Planowany termin<input name="data" type="date"></label>
<label>Liczba gości<input name="goscie" type="number" min="1" max="200" inputmode="numeric"></label>
<label class="full">Wiadomość<textarea name="wiad" placeholder="Napisz, czego potrzebujesz – oddzwonimy z odpowiedzią."></textarea></label>
<div class="full"><button class="btn dark" type="submit">Wyślij zapytanie</button> <span class="note">&nbsp;Formularz otworzy Twój program pocztowy z gotową wiadomością do {MAIL}.</span></div>
</form>'''
    doc = (head(p, 'kontakt/', 'Kontakt – Finezja, sala bankietowa Kaczki Średnie, Turek', 'Finezja Sala Bankietowa, Kaczki Średnie 10c, 62-700 Turek. Tel. 665 188 619, 601 637 397, biuro@finezja.org. Godziny otwarcia i formularz zapytania o termin.', [crumbs_ld('kontakt/', [(None, 'Kontakt')])], og='wieczor')
           + header(p, 'kontakt/') + phead(p, 'wieczor', [(None, 'Kontakt')], 'Kontakt', 'Zadzwoń, napisz albo przyjedź obejrzeć salę – pokażemy salę, plener, kuchnię i pokoje.', 'Kaczki Średnie 10c · 62-700 Turek', acts=False, short=True)
           + f'''<section class="paper"><div class="wrap"><div class="row">
<div class="txt fade"><h2 class="split" style="font-size:clamp(34px,3.8vw,56px)">Dane kontaktowe</h2>
<p class="lead">Finezja Sala Bankietowa<br>Kaczki Średnie 10c<br>62-700 Turek</p><p class="muted">NIP 7391718282</p>
<p class="lead"><a class="u" href="tel:{TEL1H}">+48 {TEL1}</a><br><a class="u" href="tel:{TEL2H}">+48 {TEL2}</a><br><a class="u" href="mailto:{MAIL}">{MAIL}</a></p>
<h3 style="margin-top:40px">Godziny otwarcia</h3><ul class="hours"><li><span>Poniedziałek</span><span>10:00–13:00</span></li><li><span>Czwartek</span><span>9:00–13:00</span></li><li><span>Piątek–niedziela</span><span>9:00–21:00</span></li></ul>
<div class="acts"><a class="btn line" href="{MAPS}" rel="noopener">Pokaż na mapie Google</a></div></div>
<div><h2 class="split" style="font-size:clamp(34px,3.8vw,56px)">Formularz kontaktowy</h2><p class="muted fade">Podaj termin, liczbę gości i okazję – odpowiemy z propozycją menu i wolnymi datami.</p>{form}</div>
</div></div></section>'''
           + cta_band(p, mapa=True) + '</main>' + footer(p))
    write('kontakt/', doc)

def polityka():
    p = '../'; bl = T['polityka-prywatnosci/']['blocks']; ctx = {'faq': [], 'used': set(), 'band': None}
    doc = (head(p, 'polityka-prywatnosci/', 'Polityka prywatności – Finezja', 'Polityka prywatności serwisu finezja.org – zasady przetwarzania danych osobowych i plików cookies.')
           + header(p, '') + phead(p, None, [(None, 'Polityka prywatności')], 'Polityka prywatności', '', acts=False)
           + f'<section class="paper body-sec"><div class="wrap narrow"><div class="prose">{render_blocks(bl, p, ctx)}</div></div></section></main>' + footer(p))
    write('polityka-prywatnosci/', doc)

# ---------------------------------------------------------------- pliki pomocnicze
def extras():
    open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0e1320"/><rect x="9" y="5" width="46" height="54" fill="none" stroke="#d2ad72" stroke-width="2"/><text x="32" y="47" text-anchor="middle" font-family="Georgia,serif" font-size="38" fill="#f4efe5">F</text></svg>')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    sm = ''.join(f'<url><loc>{BASE}{x}</loc></url>' for x in sorted(PAGES))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
    nf = (head('/finezja-sala-bankietowa/', '404.html', 'Nie ma takiej strony – Finezja', 'Strona nie istnieje.') .replace('href="/finezja-sala-bankietowa/404.html"', f'href="{BASE}"')
          + header('/finezja-sala-bankietowa/', '') + phead('/finezja-sala-bankietowa/', None, [(None, '404')], 'Tej strony już nie ma', 'Adres mógł się zmienić. Zacznij od strony głównej albo zadzwoń: ' + TEL1 + '.', acts=True) + '</main>' + footer('/finezja-sala-bankietowa/'))
    open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(nf)

def run():
    home()
    for k in SUB: sub_page(k)
    galeria(); polecamy(); kontakt(); polityka(); blog()
    for k in POSTS: post(k)
    extras()
    missing = sorted(ALLP - set(PAGES))
    print(len(PAGES), 'stron; brak:', missing)

if __name__ == '__main__':
    run()
