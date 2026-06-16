import os
import requests
from dotenv import load_dotenv
from checker import check_all_slots

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


class SlotMonitor:
    def __init__(self):
        # здесь храним последнее состояние
        self.last_state = set()

    def send_telegram(self, msg: str):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

    def format_results(self, results):
        if not results:
            return None

        msg = "📅 Nowe dostępne terminy:\n\n"

        for r in results:
            msg += f"📍 {r['location']}\n📆 {r['date']} {r['time']}\n\n"

        return msg

    def check_and_notify(self):
        results = check_all_slots()

        # превращаем результаты в "уникальные ключи"
        current_state = set(
            f"{r['location']}|{r['time']}" for r in results
        )

        # ищем новые слоты
        new_slots = current_state - self.last_state

        if new_slots:
            filtered = [
                r for r in results
                if f"{r['location']}|{r['time']}" in new_slots
            ]

            msg = self.format_results(filtered)

            if msg:
                self.send_telegram(msg)

        # обновляем состояние
        self.last_state = current_state


def main():
    monitor = SlotMonitor()
    monitor.check_and_notify()


if __name__ == "__main__":
    main()
