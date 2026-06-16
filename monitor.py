import os
import requests
from checker import check_all_slots


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


class SlotMonitor:
    def __init__(self):
        self.last_state = set()

    def send(self, msg: str):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

    def format(self, results):
        if not results:
            return None

        msg = "📅 Nowe dostępne terminy:\n\n"
        for r in results:
            msg += f"📍 {r['location']}\n📆 {r['date']} {r['time']}\n\n"
        return msg

    def run(self):
        results = check_all_slots()

        current = set(f"{r['location']}|{r['time']}" for r in results)
        new = current - self.last_state

        if new:
            filtered = [
                r for r in results
                if f"{r['location']}|{r['time']}" in new
            ]

            msg = self.format(filtered)
            if msg:
                self.send(msg)

        self.last_state = current


if __name__ == "__main__":
    SlotMonitor().run()
