from playwright.sync_api import sync_playwright

URL = "https://wizyty.uml.lodz.pl/"


def check_slots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)
        page.wait_for_timeout(5000)

        html = page.content().lower()

        browser.close()

        # временная логика (потом уточним под сайт)
        if "brak wolnych terminów" in html:
            return None

        # если есть хоть что-то — считаем что есть слот
        return "POTENTIAL_SLOT_FOUND"

LOCATIONS = [
    "Smugowa 30/32",
    "Piłsudskiego 100",
    "Krzemieniecka 2B"
]
