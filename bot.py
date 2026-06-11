import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from checker import check_slots


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот активен. Используй /next или /status")


async def next_slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = check_slots()

    if result:
        await update.message.reply_text("📅 Есть потенциальный ближайший слот")
    else:
        await update.message.reply_text("❌ Сейчас нет доступных терминов")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = check_slots()

    await update.message.reply_text(
        "🟢 Есть слоты" if result else "🔴 Нет слотов"
    )


def main():
    app = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("next", next_slot))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()


if __name__ == "__main__":
    main()
