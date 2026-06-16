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

                page.get_by_text(loc).click(timeout=5000)
                page.wait_for_timeout(3000)

                buttons = page.locator("button")

                clicked = False

                for i in range(min(buttons.count(), 40)):
                    b = buttons.nth(i)
                    txt = b.inner_text().strip()

                    if any(ch.isdigit() for ch in txt):
                        try:
                            b.click(timeout=2000)
                            clicked = True
                            break
                        except:
                            continue

                if not clicked:
                    continue

                page.wait_for_timeout(2000)

                times = page.locator("button")

                for i in range(times.count()):
                    t = times.nth(i)
                    txt = t.inner_text().strip()

                    if ":" in txt:
                        results.append({
                            "location": loc,
                            "time": txt
                        })
                        break

            except Exception as e:
                print(f"[ERROR] {loc}: {e}")

        browser.close()

    return results
