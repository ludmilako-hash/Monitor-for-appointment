import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from checker import check_all_slots

BOT_TOKEN = os.getenv("BOT_TOKEN")

# состояние (очень важно для стабильности)
monitoring = False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot started\n\n"
        "Commands:\n"
        "/check - check slots once\n"
        "/start_monitor - start auto monitoring\n"
        "/stop_monitor - stop monitoring"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = check_all_slots()

    if not results:
        await update.message.reply_text("❌ No slots")
        return

    msg = "📅 Available slots:\n\n"
    for r in results:
        msg += f"📍 {r['location']}\n⏰ {r['time']}\n\n"

    await update.message.reply_text(msg)


async def monitor_loop(app: Application):
    global monitoring

    while True:
        if monitoring:
            results = check_all_slots()

            if results:
                msg = "🚨 NEW SLOTS FOUND:\n\n"
                for r in results:
                    msg += f"📍 {r['location']}\n⏰ {r['time']}\n\n"

                await app.bot.send_message(
                    chat_id=os.getenv("CHAT_ID"),
                    text=msg
                )

        await asyncio.sleep(60)  # каждые 60 сек


async def start_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    monitoring = True
    await update.message.reply_text("🟢 Monitoring started")


async def stop_monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global monitoring
    monitoring = False
    await update.message.reply_text("🔴 Monitoring stopped")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("start_monitor", start_monitor))
    app.add_handler(CommandHandler("stop_monitor", stop_monitor))

    app.create_task(monitor_loop(app))

    app.run_polling()


if __name__ == "__main__":
    main()
