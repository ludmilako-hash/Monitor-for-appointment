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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for loc in LOCATIONS:
            try:
                page.goto(URL)
                page.wait_for_timeout(4000)

                page.get_by_text(loc).click()
                page.wait_for_timeout(3000)

                # если нет слотов
                if "brak wolnych terminów" in page.content().lower():
                    continue

                dates = page.locator("button:has-text(':') , text=/\\d{1,2}/")

                if dates.count() == 0:
                    continue

                dates.first.click()
                page.wait_for_timeout(1500)

                times = page.locator("button")

                for i in range(times.count()):
                    t = times.nth(i)
                    text = t.inner_text().strip()

                    if ":" in text and t.is_enabled():
                        results.append({
                            "location": loc,
                            "date": dates.first.inner_text().strip(),
                            "time": text
                        })
                        break

            except Exception as e:
                print(f"Error {loc}: {e}")

        browser.close()

    return results
