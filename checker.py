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

        page = browser.new_page()

        for loc in LOCATIONS:
            try:
                page.goto(URL, wait_until="networkidle")

                page.get_by_text(loc, exact=False).click()

                page.wait_for_timeout(3000)

                date_buttons = page.locator("button:visible")

                found_date = False

                for i in range(min(date_buttons.count(), 50)):
                    btn = date_buttons.nth(i)
                    text = (btn.text_content() or "").strip()

                    if any(ch.isdigit() for ch in text):
                        if btn.is_visible() and btn.is_enabled():
                            btn.click()
                            found_date = True
                            break

                if not found_date:
                    continue

                page.wait_for_timeout(2000)

                time_buttons = page.locator("button:visible")

                for i in range(time_buttons.count()):
                    t = time_buttons.nth(i)
                    text = (t.text_content() or "").strip()

                    if ":" in text and t.is_enabled():
                        results.append({
                            "location": loc,
                            "time": text,
                            "date": "selected"
                        })
                        break

            except Exception as e:
                print(f"[ERROR] {loc}: {e}")

        browser.close()

    return results
