import os
import time
import requests
from checker import check_all_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

last_state = set()


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def format(results):
    msg = "📅 Najbliższe dostępne terminy:\n\n"

    for r in results:
        msg += f"📍 {r['location']}\n📆 {r['date']} {r['time']}\n\n"

    return msg


def make_signature(results):
    return set(
        f"{r['location']}-{r['date']}-{r['time']}"
        for r in results
    )


if __name__ == "__main__":
    while True:
        try:
            results = check_all_slots()

            current = make_signature(results)

            global last_state

            # отправляем только если изменилось
            if current and current != last_state:
                send(format(results))
                last_state = current

        except Exception as e:
            print("Monitor error:", e)

        time.sleep(600)  # 10 минут
