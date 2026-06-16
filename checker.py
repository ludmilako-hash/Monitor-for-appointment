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
                page.wait_for_load_state("networkidle")

                page.get_by_text(loc, exact=False).click()
                page.wait_for_timeout(2000)

                date_buttons = page.locator("button")

                clicked = False

                for i in range(min(date_buttons.count(), 40)):
                    btn = date_buttons.nth(i)
                    text = (btn.inner_text() or "").strip()

                    if any(c.isdigit() for c in text) and btn.is_enabled():
                        btn.click()
                        clicked = True
                        break

                if not clicked:
                    continue

                page.wait_for_timeout(2000)

                times = page.locator("button")

                for i in range(times.count()):
                    t = times.nth(i)
                    text = (t.inner_text() or "").strip()

                    if ":" in text and t.is_enabled():
                        results.append({
                            "location": loc,
                            "time": text
                        })
                        break

            except:
                continue

        browser.close()

    return results
