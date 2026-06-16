from playwright.sync_api import sync_playwright

URL = "https://wizyty.uml.lodz.pl/"

LOCATIONS = [
    "Smugowa 30/32",
    "Piłsudskiego 100",
    "Krzemieniecka 2B"
]


def check_all_slots():
    results = []

    with sync_playwright() as p:
     browser = p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-dev-shm-usage"]
)

        for loc in LOCATIONS:

            try:
                page.goto(URL)
                page.wait_for_timeout(5000)

                # 1. выбрать отдел
                page.get_by_text(loc, exact=False).click()
                page.wait_for_timeout(3000)

                # 2. дождаться появления календаря (ВАЖНО)
                page.wait_for_timeout(3000)

                # 3. проверка: есть ли вообще кнопки дат
                date_buttons = page.locator("button:has-text(''), button")

                if date_buttons.count() < 5:
                    print(f"{loc}: probably not loaded calendar")
                    continue

                # 4. пробуем кликнуть первую доступную дату
                clicked = False

                for i in range(min(date_buttons.count(), 30)):
                    btn = date_buttons.nth(i)
                    text = btn.inner_text().strip()

                    if any(c.isdigit() for c in text) and btn.is_enabled():
                        btn.click()
                        clicked = True
                        break

                if not clicked:
                    continue

                page.wait_for_timeout(2000)

                # 5. ищем время
                times = page.locator("button")

                for i in range(times.count()):
                    t = times.nth(i)
                    text = t.inner_text().strip()

                    if ":" in text and t.is_enabled():
                        results.append({
                            "location": loc,
                            "time": text,
                            "date": "selected"
                        })
                        break

            except Exception as e:
                print(f"Error {loc}: {e}")

        browser.close()

    return results
