import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://wizyty.uml.lodz.pl"


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}
    )


def check():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        page.wait_for_timeout(8000)

        html = page.content().lower()

        browser.close()
        return html


def found_slots(html):
    return "brak wolnych termin" not in html


if __name__ == "__main__":
    html = check()

    if found_slots(html):
        send("🚨 Возможны свободные термины в Łódź! Проверь сайт: https://wizyty.uml.lodz.pl")
