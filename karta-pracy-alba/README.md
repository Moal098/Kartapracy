# Karta pracy kierowcy — PTS ALBA Chorzów (wersja 4.5 — test na rejonie)

Aplikacja mobilna (PWA) do prowadzenia karty pracy kierowcy: logowanie PIN-em, kontrola pojazdu (OC), przebieg zmiany jednym przyciskiem, rejestracja wysypania odpadów, tankowanie, rozliczenie czasu na MPK, podpis i eksport karty.

Cała aplikacja to jeden plik `index.html`. Dane karty są zapisywane wyłącznie w pamięci telefonu (localStorage) — nie ma serwera.

> **Uwaga — dane osobowe.** `index.html` zawiera listę pracowników z PIN-ami (sekcja `APP_DATA`). W repozytorium **publicznym** i na publicznym GitHub Pages każdy może je odczytać. Do testów użyj repozytorium prywatnego albo podmień listę `pracownicy` na dane testowe.

> **„Wyślij kartę" nic nie przesyła.** Przycisk zamyka kartę (tylko do odczytu) i otwiera podsumowanie do udostępnienia (e-mail, komunikator). Przesyłanie do systemu kierownika wymaga backendu — poza zakresem tej wersji.

## Zawartość paczki

| Plik | Do czego |
|---|---|
| `index.html` | Aplikacja (HTML + CSS + JS w jednym pliku) |
| `manifest.webmanifest` | Instalacja na ekranie głównym telefonu |
| `sw.js` | Praca offline (service worker) |
| `icons/` | Ikony aplikacji |
| `.nojekyll` | GitHub Pages serwuje pliki bez przetwarzania |
| `CHANGELOG.md` | Lista zmian |
| `docs/SCENARIUSZ_TESTOW.md` | Lista kontrolna dla testerów |
| `tests/smoke_test.py` | Automatyczny test pełnej zmiany (opcjonalny, Playwright; czas przewijany zegarem testu, nie aplikacji) |
| `tests/fixtures/` | Zdjęcie dla testu automatycznego |

## Publikacja na GitHub Pages

1. Na GitHubie: **New repository** → nazwa np. `karta-pracy-alba` → zalecane **Private**.
2. **Add file → Upload files** → przeciągnij **zawartość** tego folderu (nie sam folder; `index.html` ma leżeć w katalogu głównym repozytorium) → **Commit changes**.
   Plik `.nojekyll` bywa ukryty w systemie — jeśli się nie wgrał, utwórz go przez **Add file → Create new file** (pusty).
3. **Settings → Pages** → *Source*: **Deploy from a branch** → *Branch*: `main`, folder `/ (root)` → **Save**.
4. Po 1–2 minutach aplikacja będzie pod adresem `https://<konto>.github.io/karta-pracy-alba/`.

Pages w repozytorium prywatnym wymaga płatnego planu GitHub (Pro / Team / Enterprise). Na planie darmowym strona z repozytorium prywatnego nie zostanie opublikowana.

### Instalacja na telefonie (Android, Chrome)

Otwórz adres → menu ⋮ → **Dodaj do ekranu głównego / Zainstaluj aplikację**. Po pierwszym uruchomieniu z internetem aplikacja działa także offline.

### Aktualizacja wersji

1. Wgraj nowy `index.html`.
2. W `sw.js` zmień `CACHE` (np. `karta-pracy-alba-v4.5.1`).
3. Na telefonie aplikacja pobierze nową wersję w tle — **zamknij ją i otwórz ponownie** (czasem dwa razy). Numer wersji jest na ekranie logowania.

### Test lokalny bez GitHuba

Plik `index.html` można otworzyć wprost w przeglądarce (bez pracy offline). Z działającym service workerem:

```
python -m http.server 8000
```
i otwórz `http://localhost:8000`.

## PIN-y testowe

| PIN | Kierowca | Rejon (frakcja) |
|---|---|---|
| 1234 | Dariusz Bogusiewicz | HLZ — zmieszane |
| 0420 | Krzysztof Bonk | HLP — papier |
| 0580 | Henryk Broda | HLM — metale i tworzywa |
| 2222 | Michał Czyba | HLS — szkło |
| 0710 | Dariusz Dominiczak | HLK — bio |

## Wersja do testów na rejonie

Ta wersja działa **wyłącznie w czasie rzeczywistym** — usunięty jest tryb testowy (przyspieszony zegar, zdjęcia zastępcze bez aparatu, automatyczne domykanie karty). Zdjęcia OC robi się aparatem telefonu, podpis składa się palcem.

Karty zapisane w telefonie przez starszą wersję z trybem testowym po wznowieniu również liczą czas rzeczywisty.

## Zasady rozliczeń (konfiguracja w `APP_DATA`)

### Kod odpadu z rejonu

Po wyborze rejonu kod odpadu do wysypania ustawia się automatycznie i nie można go zmienić. Wpis z innym kodem (np. z karty zapisanej w starszej wersji) jest oznaczany jako rozbieżność i blokuje wysłanie karty.

| Rejon | Kod | Pole |
|---|---|---|
| HLZ | 20 03 01 | `APP_DATA.rejony[].kod_odpadu` |
| HLP | 20 01 01 | |
| HLM | 20 01 39 | |
| HLS | 20 01 02 | |
| HLK | 20 01 08 | |

Kody przyjęte z dotychczasowego opisu frakcji (pierwszy kod) — **do potwierdzenia** z praktyką sprawozdawczą.

### Ilość

Jedyna jednostka: **Mg** (3 miejsca po przecinku, przecinek lub kropka). Wartość ≥ 100 jest traktowana jako pomyłka (kg) i blokowana z podpowiedzią przeliczenia; powyżej 15 Mg — ostrzeżenie.

### MPK

Przypisanie czynności → MPK: `APP_DATA.czynnosci`. Nazwy kont: `APP_DATA.mpk`.

| MPK | Czynności |
|---|---|
| 255000 | Serwis / awaria |
| 255001 | Obsługa codzienna (OC — liczona automatycznie od potwierdzenia zmiany do „Rozpocznij zmianę"), tankowanie ON/CNG, mycie, sprzątanie |
| 255002 | Oczekiwanie na pojazd, oczekiwanie na współpracowników |
| 255003 | Dojazd Żory |
| 255004 | Przerwy (śniadaniowa, inna), szkolenie BHP |
| *MPK rejonu* | Dojazd, zbiórka, rozładunek na sortowni, postój w bazie — pole `APP_DATA.rejony[].mpk` (**puste — do uzupełnienia**) |

Szkolenie BHP trafia na 255004, ale **nie jest odliczane** od czasu pracy (przerwy są).

## Znane ograniczenia

- Brak backendu — karta żyje w telefonie do czasu „Nowa zmiana" lub upływu 20 h.
- Zdjęcia OC są zapisywane w localStorage; przy braku miejsca aplikacja zapisuje kartę bez zdjęć (komunikat na ekranie).
- QR wymaga przeglądarki z `BarcodeDetector` (Chrome Android), NFC — Chrome Android z Web NFC.
- Godzina w polu „Godzina zakończenia" wyświetla się w formacie systemu telefonu (12/24 h).
