import os
import requests
from checker import check_all_slots
from telegram.ext import Application, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")


def format_results(results):
    if not results:
        return "❌ Нет доступных терминов"

    msg = "📅 Найденные термины:\n\n"

    for r in results:
        msg += f"📍 {r['location']}\n🕒 {r['time']}\n\n"

    return msg


async def start(update, context):
    await update.message.reply_text(
        "Привет! Напиши /check чтобы проверить слоты"
    )


async def check(update, context):
    await update.message.reply_text("🔄 Проверяю...")

    results = check_all_slots()

    await update.message.reply_text(format_results(results))


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
