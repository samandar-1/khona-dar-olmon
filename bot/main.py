import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.core.startup import on_startup
from bot.core.commands import set_commands

from bot.conversations.new_ad.flow import new_ad_conv
from bot.conversations.new_ad.handlers import check_subscription_callback
from bot.conversations.admin_handlers import admin_dashboard, admin_pending_ads, admin_approved_ads, admin_action_callback #, admin_check_ads, admin_ad_callback
from bot.conversations.my_ads_handlers import show_my_ads, delete_ad_handler
from telegram.ext import CommandHandler, CallbackQueryHandler

# ENV
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN fehlt")

# App
app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

# Admin
# app.add_handler(CommandHandler("admin_ads", admin_check_ads))
# app.add_handler(CallbackQueryHandler(admin_ad_callback, pattern="^(approve|reject):"))

app.add_handler(CommandHandler("admin", admin_dashboard))

app.add_handler(CallbackQueryHandler(admin_pending_ads, pattern="^admin:pending$"))
app.add_handler(CallbackQueryHandler(admin_approved_ads, pattern="^admin:approved$"))

app.add_handler(
    CallbackQueryHandler(
        admin_action_callback,
        pattern="^(approve|reject|delete):"
    )
)

# My Ads
app.add_handler(CommandHandler("show_my_ads", show_my_ads))
app.add_handler(delete_ad_handler)

# Conversations
app.add_handler(new_ad_conv)
app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern="^check_sub$"))


# Run
if __name__ == "__main__":
    print("🤖 Bot läuft...")
    app.run_polling()
