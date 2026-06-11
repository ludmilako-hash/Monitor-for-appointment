import os

print("STARTING BOT")

try:
    import requests
    print("REQUESTS OK")
except Exception as e:
    print("IMPORT ERROR:", e)
    raise

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

print("TOKEN:", "OK" if BOT_TOKEN else "MISSING")
print("CHAT:", CHAT_ID)

URL = "https://wizyty.uml.lodz.pl"

def check():
    r = requests.get(URL, timeout=30)
    return r.text.lower()

def send(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing credentials")
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text}
    )

if __name__ == "__main__":
    try:
        html = check()
        print("SITE LOADED")

        if "brak wolnych termin" not in html:
            print("SLOTS POSSIBLE")
            send("🚨 Возможны слоты в Łódź!")
        else:
            print("NO SLOTS")

    except Exception as e:
        print("ERROR:", e)
        raise
