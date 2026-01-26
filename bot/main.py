import os
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from bot.conversations.new_ad.handlers import (
    new_ad_start,
    new_ad_title,
    new_ad_type_callback,
    new_ad_type_callback2,
    new_ad_kaltmiete,
    new_ad_nebenkosten,
    new_ad_raumflaeche,
    new_ad_stadt,
    new_ad_anmeldung_callback,
    new_ad_start_date,
    new_ad_end_date,
    new_ad_bilder,
    new_ad_finish,
)
from bot.conversations.my_ads.handlers import (
    show_my_ads,
    delete_ad_callback,
)

from bot.conversations.new_ad.states import NewAdState
from bot.conversations.admin.handlers import admin_check_ads, admin_ad_callback
from db.database import init_db
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# =====================
# ENV
# =====================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN nicht gefunden")


# =====================
# POST INIT (ASYNC)
# =====================
async def on_startup(app):
    await init_db()
    print("🤖 Bot läuft...")

# =====================
# APP
# =====================
# request = HTTPXRequest(connect_timeout=30, read_timeout=30)
app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .post_init(on_startup)
    .build()
)

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("new_ad", "📝 Neue Anzeige erstellen"),
        BotCommand("show_my_ads", "📄 Meine Anzeigen"),
        BotCommand("admin_ads", "🛠 Anzeigen prüfen (Admin)")
    ])
# =====================
# ADMIN
# =====================
app.add_handler(CommandHandler("admin_ads", admin_check_ads))
app.add_handler(CommandHandler("show_my_ads", show_my_ads))
app.add_handler(CommandHandler("start", new_ad_start))
app.add_handler(CallbackQueryHandler(admin_ad_callback, pattern="^(approve|reject):"))

# =====================
# CONVERSATION
# =====================
new_ad_conv = ConversationHandler(
    entry_points=[CommandHandler("new_ad", new_ad_start),
                  CommandHandler("start", new_ad_start)],
    states={

        NewAdState.VERMIETUNG_ART: [
            CallbackQueryHandler(new_ad_type_callback)
        ],
        NewAdState.AD_TYPE: [
            CallbackQueryHandler(new_ad_type_callback2)
        ],
        NewAdState.STADT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_stadt)
        ],
        NewAdState.KALTMIETE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_kaltmiete)
        ],
        NewAdState.NEBENKOSTEN: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_nebenkosten)
        ],
        NewAdState.RAUMFLAECHE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_raumflaeche)
        ],
        NewAdState.ANMELDUNG: [
            CallbackQueryHandler(new_ad_anmeldung_callback)
        ],
        NewAdState.START_DATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_start_date)
        ],
        NewAdState.END_DATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_end_date)
        ],
        NewAdState.BILDER: [
            MessageHandler(filters.PHOTO, new_ad_bilder),
            CommandHandler("finish", new_ad_finish),
        ],
        NewAdState.TITLE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_title)
        ],
    },
    fallbacks=[
        CommandHandler("new_ad", new_ad_start)
    ],
    allow_reentry=True
)

app.add_handler(new_ad_conv)

# =====================
# RUN (SYNC!)
# =====================
if __name__ == "__main__":
    app.post_init = set_commands
    print("🤖 Bot läuft...")
    app.run_polling()