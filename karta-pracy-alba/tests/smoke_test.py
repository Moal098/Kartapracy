"""Test dymny wersji na rejon: pełna zmiana HLZ w czasie rzeczywistym aplikacji.

Czas jest przewijany zegarem Playwright (page.clock) — aplikacja nie ma już
trybu przyspieszonego. Zdjęcia OC podawane przez okno wyboru pliku.

Uruchomienie:
    pip install playwright && playwright install chromium
    python tests/smoke_test.py
Zrzuty ekranów: tests/screenshots/
"""
import asyncio, os, datetime
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
APP = 'file://' + os.path.abspath(os.path.join(HERE, '..', 'index.html'))
PHOTO = os.path.join(HERE, 'fixtures', 'zdjecie_testowe.jpg')
OUT = os.path.join(HERE, 'screenshots')
os.makedirs(OUT, exist_ok=True)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
        await pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        await pg.clock.install(time=datetime.datetime(2026, 12, 1, 6, 0, 0))
        await pg.goto(APP)

        async def mins(n):                       # przewiń czas o n minut
            await pg.clock.run_for(n * 60 * 1000)

        async def shot(name):
            await pg.screenshot(path=os.path.join(OUT, name + '.png'), full_page=True)

        async def km_modal(value):
            if await pg.evaluate("document.getElementById('kmm').classList.contains('show')"):
                if value is None:
                    await pg.click('#kmm-skip')
                else:
                    await pg.fill('#kmm-in', str(value)); await pg.click('#kmm-ok')

        async def step(selector, km=None, after=0):
            await pg.click(selector); await km_modal(km); await mins(after)

        # ── logowanie i konfiguracja ──
        for k in '1234':
            await pg.click(f'#pinpad [data-k="{k}"]')
        await pg.click('#pinpad [data-k="ok"]')
        await pg.click('#vp-grid .vp-card >> nth=1')
        await pg.click('.fr-tile >> nth=0')
        await pg.click('.tr-opt >> nth=0')
        await shot('01_setup')
        await pg.click('#setup-btn')

        # ── OC: 9 punktów + 4 zdjęcia z pliku ──
        for i in range(9):
            await pg.click(f'#oc-list .check-item >> nth={i}')
        for i in range(4):
            async with pg.expect_file_chooser() as fc:
                await pg.click(f'#ph{i}')
            await (await fc.value).set_files(PHOTO)
            await pg.wait_for_function(f"document.querySelector('#ph{i} img') !== null")
        assert not await pg.is_disabled('#oc-btn'), 'OC nie odblokował startu'
        await mins(12)
        await pg.click('#oc-btn')

        # ── przebieg ──
        await pg.evaluate("go('s-czynnosci')")
        await step('#fl-next', 125008, 15)        # wyjazd na rejon
        await step('#fl-next', 125010, 150)       # zbiórka
        await step('#fl-next', 125030, 15)        # dojazd do sortowni
        await step('#fl-next', 125034, 10)        # rozładunek
        await pg.click('#fl-other'); await pg.click('.fl-alt[data-x="tank"]')
        await km_modal(125037); await mins(12)    # tankowanie w trakcie rozładunku
        await shot('02_tankowanie')
        await step('#fl-next', 125040, 5)         # wróć: rozładunek
        await pg.click('#fl-break'); await pg.click('.fl-alt[data-b="sniad"]'); await mins(15)
        await step('#fl-next', None, 5)           # koniec przerwy → rozładunek
        await step('#fl-next', 125045, 15)        # powrót na rejon
        await step('#fl-next', 125047, 120)       # zbiórka
        await step('#fl-second', 125060, 15)      # zjazd do bazy
        await step('#fl-next', 125062, 10)        # postój w bazie
        txt = await pg.evaluate("document.getElementById('fl-kurs').textContent")
        assert 'rozładunków: 1' in txt, 'tankowanie/przerwa utworzyły dodatkowy rozładunek: ' + txt
        await shot('03_czynnosci')

        # ── odpady ──
        await pg.evaluate("go('s-odpady')")
        await pg.fill('#odp-qty', '8420')
        assert await pg.is_disabled('#odp-add'), 'kg nie zostały zablokowane'
        await pg.fill('#odp-qty', '8,42'); await pg.click('#odp-add')
        await shot('04_odpady')

        # ── paliwo ──
        await pg.evaluate("go('s-tankowanie')")
        await pg.fill('#km-after', '125063'); await pg.fill('#fuel-qty', '60')
        await pg.evaluate("calcKmDiff();calcFuelMeter();updTankBtn()")
        await pg.click('#tank-save'); await pg.clock.run_for(1000)

        # ── zakończenie ──
        await pg.evaluate("go('s-czynnosci')")
        await step('#fl-next', None)              # zakończ zmianę
        await pg.clock.run_for(500)
        await pg.evaluate("document.getElementById('v3-sign-canvas').scrollIntoView({block:'center'})")
        await pg.clock.run_for(200)
        box = await pg.locator('#v3-sign-canvas').bounding_box()
        await pg.mouse.move(box['x'] + 30, box['y'] + 80); await pg.mouse.down()
        for i in range(10):
            await pg.mouse.move(box['x'] + 30 + i * 25, box['y'] + 80 + (15 if i % 2 else -15))
        await pg.mouse.up()
        await shot('05_zakonczenie')
        why = await pg.evaluate("document.getElementById('send-why').textContent")
        assert not await pg.is_disabled('#send-btn'), 'wysyłka zablokowana: ' + why
        await pg.click('#send-btn'); await pg.clock.run_for(1000)
        summ = await pg.evaluate("document.getElementById('v3-modal-text').value")
        assert 'ROZLICZENIE MPK' in summ and '255001' in summ and '255004' in summ, 'brak rozliczenia MPK'
        assert '8,420 Mg' in summ, 'brak wpisu w Mg'
        assert 'Kod odpadu: 20 03 01' in summ, 'zły kod odpadu'
        assert 'Start: 06:00' in summ, 'zegar nie jest rzeczywisty'
        await pg.click('#v3-modal-x'); await shot('06_wyslana')
        assert not errs, errs
        print(summ)
        print('\nOK — test dymny zakończony bez błędów')
        await b.close()

asyncio.run(main())
