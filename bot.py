import os
import json
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

STATE_FILE = "state.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"monitor": False, "last": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def run_checker():
    result = subprocess.check_output(["python", "checker.py"])
    return result.decode("utf-8")


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Проверяю...")

    output = run_checker()

    await update.message.reply_text(f"Результат:\n{output}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    await update.message.reply_text(f"Мониторинг: {'ON' if state.get('monitor') else 'OFF'}")


async def start_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    state["monitor"] = True
    save_state(state)
    await update.message.reply_text("🟢 Мониторинг включён (через GitHub Actions cron)")


async def stop_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    state["monitor"] = False
    save_state(state)
    await update.message.reply_text("🔴 Мониторинг выключен")


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = load_state()
    await update.message.reply_text(str(state.get("last", [])))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("startmonitor", start_monitor))
    app.add_handler(CommandHandler("stopmonitor", stop_monitor))
    app.add_handler(CommandHandler("last", last))

    app.run_polling()


if __name__ == "__main__":
    main()
