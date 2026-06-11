import os
import json
import requests
from checker import check_all_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def normalize(slot):
    # делаем уникальный "ключ" слота
    return f"{slot['location']}|{slot['date']}|{slot['time']}"


def format_slots(slots):
    msg = "🆕 Nowe wolne terminy:\n\n"
    for s in slots:
        msg += f"📍 {s['location']}\n📅 {s['date']} {s['time']}\n\n"
    return msg


if __name__ == "__main__":
    current = check_all_slots()
    previous = load_state()

    current_keys = {normalize(s): s for s in current}
    previous_keys = set(previous)

    # находим только НОВЫЕ слоты
    new_slots = [
        s for k, s in current_keys.items()
        if k not in previous_keys
    ]

    if new_slots:
        send_message(format_slots(new_slots))

    # обновляем состояние ВСЕГДА
    save_state(list(current_keys.keys()))
