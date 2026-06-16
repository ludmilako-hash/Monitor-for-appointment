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
                page.goto(URL, timeout=60000)
                page.wait_for_load_state("networkidle")

                # выбрать локацию
                page.get_by_text(loc).click(timeout=5000)
                page.wait_for_timeout(3000)

                # ищем кликабельные даты
                date_buttons = page.locator("button")

                found_date = False

                for i in range(min(date_buttons.count(), 40)):
                    btn = date_buttons.nth(i)
                    text = btn.inner_text().strip()

                    if any(ch.isdigit() for ch in text):
                        try:
                            btn.click(timeout=2000)
                            found_date = True
                            break
                        except:
                            continue

                if not found_date:
                    continue

                page.wait_for_timeout(2000)

                # ищем время
                time_buttons = page.locator("button")

                for i in range(time_buttons.count()):
                    t = time_buttons.nth(i)
                    text = t.inner_text().strip()

                    if ":" in text:
                        results.append({
                            "location": loc,
                            "time": text
                        })
                        break

            except Exception as e:
                print(f"[ERROR] {loc}: {e}")

        browser.close()

    return results
