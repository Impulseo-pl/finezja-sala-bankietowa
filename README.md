# Finezja — demo v4 (sala bankietowa pod Turkiem)

Lead z kampanii (Mariusz). Strona klienta: https://www.finezja.org/ · Demo: https://impulseo-pl.github.io/finezja-sala-bankietowa/ (sprawdzamy **zawsze z `?team=1`**).
Poprzednie dema bez zmian: `Impulseo-pl/finezja` (v1), `finezja-turek` (automat), `finezja-sala` (v3, wino + krem).

Treść: świeży zrzut finezja.org z 26.10.2026 (`_src/wyciagnij.py` → `_src/tresci.json`), 39 adresów jak na ich stronie (23 strony + 16 wpisów).
Szkicowe wstawki z ich strony („[ogród / staw / altana]”, „– uzupełnij”) poprawione w `FIX` w `_src/build.py`. Stocki zastąpione prawdziwymi zdjęciami sali.

Styl: nocny granat z ich wieczornego filmu + złoto okien, Ibarra Real Nova + Albert Sans, zdjęcia w naturalnych proporcjach.
Ruch: drzwi sali otwierające się przy wejściu i zamykające przy przejściu na podstronę, Lenis, nagłówki odsłaniane słowami, wideo w hero,
przyklejone zdjęcia przy opisie sali, zdjęcie płynące za kursorem na liście przyjęć, liczniki, stopklatka, linia procesu, FAQ, galeria z powiększeniem, mapa OSM.

Budowanie: `python _src/obrazy.py` (raz) i `python _src/build.py`. Zrzuty: `python _src/shots.py home,wesele/ 1440` (bez serwera).
