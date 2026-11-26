# Lista zmian

## 4.5 — test na rejonie

### Wersja polowa
- Usunięty tryb testowy: przyspieszony zegar (1 s = 5 min), zdjęcia zastępcze OC i automatyczne domykanie karty przy eksporcie. Aplikacja liczy wyłącznie czas rzeczywisty; flaga trybu testowego z kart zapisanych starszą wersją jest ignorowana.
- Test automatyczny przewija czas zegarem Playwright i podaje zdjęcia przez okno wyboru pliku.

### Odpady
- Kod odpadu przypisywany automatycznie z rejonu (`kod_odpadu`), bez możliwości zmiany na karcie; rozbieżność kodu blokuje wysłanie.
- Ilość wyłącznie w Mg; wykrywanie wpisów w kg; migracja starszych wpisów kg → Mg przy wznowieniu karty.
- Wpis przypisany do kursu; usuwanie wpisów; domyślne miejsce wysypania = sortownia rejonu.
- Rozładunek przerwany przerwą lub tankowaniem nie tworzy nowego kursu (kursy liczone z przebiegu).

### MPK i czynności
- Nowe czynności dodatkowe: serwis/awaria, tankowanie, mycie, sprzątanie, oczekiwanie na pojazd, oczekiwanie na współpracowników, dojazd Żory, szkolenie BHP.
- Czynności dodatkowe i przerwy wstrzymują bieżący krok i wracają do niego (także łańcuchowo).
- Czas kontroli OC zapisywany automatycznie jako czynność (255001).
- Usunięta przerwa „techniczna" (mieszała tankowanie z serwisem).
- Rozliczenie MPK w Czynnościach, na ekranie zakończenia, w eksporcie tekstowym i JSON; wykrywanie czasu nieprzypisanego.

### Zakończenie karty
- Naprawiony układ: pole godziny i „Teraz" nie nachodzą na siebie, podpis mieści się w karcie.
- Jedna walidacja zasila postęp, listę kontrolną i przycisk wysyłki; widać, czego brakuje.
- Zamykanie czynności w toku jednym przyciskiem; podpowiedź godziny z końca ostatniej czynności.
- Godzina zakończenia nie może być wcześniejsza niż koniec ostatniej czynności; obsługa przejścia przez północ.
- Podpis zapisuje się po każdym pociągnięciu (bez osobnego „Zatwierdź").
- Po wysłaniu karta jest tylko do odczytu.

### Inne
- Paczka PWA: manifest, service worker (offline), ikony.
- Poprawiony niedomknięty znacznik HTML na ekranie logowania.
