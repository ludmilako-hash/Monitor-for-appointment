import os
import requests
from checker import check_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


if __name__ == "__main__":
    result = check_slots()

    if result:
        send("📅 Найден возможный свободный термин в UM Łódź!")
    else:
        print("No slots")
