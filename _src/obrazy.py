# -*- coding: utf-8 -*-
"""Nowe zdjęcia i grafiki z finezja.org (zrzut 26.10) -> img/<nazwa>-<szer>.webp. Zdjęcia sali z dema v3 są już w img/."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw'); OUT = os.path.join(os.path.dirname(HERE), 'img')
NOWE = {
    'zespol': '20241203_132533-1-1.webp',
    'sala-nowa': 'Sala-bankietowa-Finezja.webp',
    'catering-bufet': 'ile-kosztuje-catering-na-20-osob-widelki-cenowe-i-przyklady-1.webp',
    'plakat-andrzejki': 'Bal_Andrzejkowy_2026_Plakat_1_-1.png',
    'plakat-karnawal': 'Bal_Karnawalowy_2026.png',
    'plakat-noworoczny': 'Bal_noworoczny_2025-2026.png',
    'menu-catering-1': '2.png',
    'menu-catering-2': 'catering-brudzew.webp',
    'menu-wigilia-firmowa': 'wigilia-firmowa-2026-menu-ceny-turek-1.webp',
    'osiemnastka-kroki': 'Jak-przygotowac-18-krok-po-kroku.webp',
    'kpo': 'FE_RP_UE_KPO_rgb_kolor_poziom_jpg.webp',
    # większe oryginały pionowych zdjęć, które w v3 były tylko w 640 px
    'osiemnastka': 'konin-osiemnastka.webp', 'scianka-mis': 'dj-na-wesele-turek-scianka.webp', 'dek-stol': 'przyjecia-weselne.webp',
    'sala-pion': 'lokal-na-wesele-konin.webp', 'nakrycie': 'wesela-sala.webp', 'dek-oltarz': 'Dekoracje-restauracji.webp',
    'dek-milosc': 'sala-weselna-1.webp', 'dek-balony': 'sala-weselna-turek.webp',
}
for name, fn in NOWE.items():
    im = Image.open(os.path.join(RAW, fn)).convert('RGB')
    for w in (640, 1100, 1600):
        if im.width <= w:
            if w == 640 or im.width > 640 + 100: im.save(os.path.join(OUT, f'{name}-{im.width}.webp'), quality=82, method=6)
            break
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(os.path.join(OUT, f'{name}-{w}.webp'), quality=82, method=6)
    print(name, im.size)
