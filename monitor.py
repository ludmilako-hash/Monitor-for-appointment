import os
import json
import requests
from checker import check_all_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def format_results(results):
    if not results:
        return None

    msg = "📅 Найдены доступные слоты:\n\n"
    for r in results:
        msg += f"📍 {r['location']}\n⏰ {r['time']}\n\n"
    return msg


def main():
    results = check_all_slots()

    print("DEBUG RESULTS:", results)

    state = load_state()
    new_state = {}

    messages = []

    for r in results:
        key = f"{r['location']}|{r['time']}"
        new_state[key] = True

        if key not in state:
            messages.append(r)

    if messages:
        send(format_results(messages))
        save_state(new_state)
    else:
        print("No new slots")


if __name__ == "__main__":
    main()
