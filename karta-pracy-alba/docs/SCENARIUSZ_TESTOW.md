# Scenariusz testów na rejonie — wersja 4.5

Test prowadzony w normalnej zmianie, w czasie rzeczywistym. Na ekranie logowania musi być napis „wersja 4.5 · test na rejonie".

Zaznaczaj ☐ → ☑. Przy błędzie zapisz: krok, co się stało, zrzut ekranu.

## A. Start zmiany
- ☐ PIN 1234 → ekran konfiguracji z imieniem kierowcy.
- ☐ Wybór pojazdu; skan QR / wpisanie numeru ręcznie znajduje pojazd.
- ☐ Frakcja HLZ → trasa HLZ1: w podsumowaniu widać „kod 20 03 01", załoga zaznaczona automatycznie.
- ☐ Kontrola pojazdu: 9 punktów + min. 4 zdjęcia aparatem → „Rozpocznij zmianę".
- ☐ Na ekranie kontroli i przy eksporcie nie ma przełącznika „Tryb testowy"; zegar w Czynnościach pokazuje bieżącą godzinę.

## B. Przebieg i MPK
- ☐ Czynności: Wyjazd na rejon → Rozpocznij zbiórkę → Dojazd do sortowni → Rozładunek.
- ☐ Na liście przebiegu pierwsza pozycja to „Obsługa codzienna (OC)" z MPK 255001.
- ☐ W trakcie rozładunku: Inny krok → Tankowanie → przycisk „Wróć: Rozładunek". Licznik rozładunków nadal 1.
- ☐ Przerwa → Śniadaniowa → Koniec: powrót do poprzedniego kroku.
- ☐ Przerwa → Szkolenie BHP, potem Inny krok → Oczekiwanie na współpracowników → „Wróć" prowadzi do kroku sprzed BHP.
- ☐ Każda czynność dodatkowa ma właściwe MPK (tabela w README).
- ☐ Podsumowanie w Czynnościach pokazuje rozbicie na MPK.

## C. Odpady
- ☐ Ekran Odpady: kod 20 03 01 zablokowany, bez możliwości wyboru innego.
- ☐ Wpis „8420" → komunikat o kilogramach, przycisk nieaktywny.
- ☐ Wpis „8,42" → zapisane 8,420 Mg, kurs 1.
- ☐ Usunięcie wpisu działa (z potwierdzeniem).
- ☐ Zmiana z PIN-em 0420 (HLP) → kod 20 01 01.

## D. Zakończenie
- ☐ „Zakończ zmianę" z przebiegu → godzina wstawiona automatycznie.
- ☐ Wejście przez „Zakończ zmianę" na ekranie głównym przy trwającej czynności → walidacja „Czynność w toku" z przyciskiem „Zamknij o …".
- ☐ Godzina wcześniejsza niż ostatnia czynność → czerwony komunikat, wysyłka zablokowana.
- ☐ Pole godziny i „Teraz" w jednym wierszu, nic na siebie nie nachodzi (także w trybie rękawic).
- ☐ Podpis palcem → „podpisano · GG:MM", bez dodatkowego zatwierdzania; „Wyczyść" cofa.
- ☐ Pod przyciskiem wysyłki widać listę braków; po uzupełnieniu przycisk aktywny.
- ☐ Po wysłaniu: podsumowanie zawiera sekcje „ROZLICZENIE MPK" i „ODPADY" w Mg; godzina i podpis zablokowane.

## E. Odporność
- ☐ Wygaszenie ekranu na 10+ min w trakcie zbiórki → po odblokowaniu czas czynności jest zgodny z zegarkiem.
- ☐ W połowie zmiany zamknij przeglądarkę → po otwarciu baner „Niezakończona karta" → Wznów: przebieg, odpady i czynność w toku odtworzone.
- ☐ Tryb samolotowy po instalacji: aplikacja się uruchamia (wymaga GitHub Pages / https).
