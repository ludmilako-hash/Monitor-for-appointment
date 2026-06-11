import os
import requests
from checker import check_all_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def format(results):
    if not results:
        return "❌ Нет доступных терминов"

    msg = "📅 Najbliższe dostępne terminy:\n\n"

    for r in results:
        msg += f"📍 {r['location']}\n📆 {r['date']} {r['time']}\n\n"

    return msg


if __name__ == "__main__":
    results = check_all_slots()
    send(format(results))
    
