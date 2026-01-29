import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.core.startup import on_startup
from bot.core.commands import set_commands

from bot.conversations.new_ad.flow import new_ad_conv
from bot.conversations.admin_handlers import admin_check_ads, admin_ad_callback
from bot.conversations.my_ads_handlers import show_my_ads, delete_ad_handler
from telegram.ext import CommandHandler, CallbackQueryHandler

# ENV
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN fehlt")

# App
app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()

# Commands
app.post_init = set_commands

# Admin
app.add_handler(CommandHandler("admin_ads", admin_check_ads))
app.add_handler(CallbackQueryHandler(admin_ad_callback, pattern="^(approve|reject):"))

# My Ads
app.add_handler(CommandHandler("show_my_ads", show_my_ads))
app.add_handler(delete_ad_handler)

# Conversations
app.add_handler(new_ad_conv)

# Run
if __name__ == "__main__":
    print("🤖 Bot läuft...")
    app.run_polling()
