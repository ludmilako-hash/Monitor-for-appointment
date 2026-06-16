import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from checker import check_all_slots

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋\n"
        "Команды:\n"
        "/check — проверить слоты сейчас"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Проверяю... ⏳")

    results = check_all_slots()

    if not results:
        await update.message.reply_text("❌ Нет доступных терминов")
        return

    msg = "📅 Найдены слоты:\n\n"
    for r in results:
        msg += f"📍 {r['location']}\n🕒 {r['time']}\n\n"

    await update.message.reply_text(msg)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()


if __name__ == "__main__":
    main()
