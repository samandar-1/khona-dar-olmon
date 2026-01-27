from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db.database import AsyncSessionLocal
from db.controllers.ad_controller import get_ad_by_id
from db.models import Ad
import asyncio
from sqlalchemy import text
import json
import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
# /my_ads Command
async def show_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(
            "SELECT id, title, type, telegram_message_id, approved FROM ads WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        ads = result.fetchall()

    if not ads:
        await update.message.reply_text("Du hast noch keine Anzeigen.")
        return

    for ad in ads:
        ad_id, title, ad_type, msg_ids_json, approved = ad
        reply_text = f"ID: {ad_id}\nBeschreibung: {title}\nTyp: {ad_type}"
        keyboard = [
            [InlineKeyboardButton("Löschen ❌", callback_data=f"delete_ad:{ad_id}")]
        ]

        if approved:
            reply_text += "\nStatus: im Kanal veröffentlicht"

            # msg_ids = json.loads(msg_ids_json)
            print("1", msg_ids_json)
            if msg_ids_json:
                try:
                    msg_ids = json.loads(msg_ids_json)
                    if isinstance(msg_ids, str):
                        msg_ids = json.loads(msg_ids)
                    print("2, type", type(msg_ids)) # das kommt aber str type
                    link = f"https://t.me/{CHANNEL_USERNAME}/{msg_ids[0]}"
                    print("3", link)
                    reply_text += f"\nLink🔗: {link}"
                except json.JSONDecodeError:
                    print("No msg id")

        else:
            reply_text += f"\nStatus: in Prüfung"

        await update.message.reply_text(
            reply_text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Callback für Löschen


async def delete_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("test0")
    query = update.callback_query
    await query.answer()

    ad_id = int(query.data.split(":")[1])
    user_id = query.from_user.id
    print("test1")

    async with AsyncSessionLocal() as session:

        # --- Anzeige holen ---
        ad = await session.get(Ad, ad_id)
        if not ad or ad.user_id != user_id:
            await query.edit_message_text("❌ Keine Berechtigung oder Anzeige existiert nicht.")
            return

        # --- Telegram Channel Messages löschen ---
        if ad.telegram_message_id:
            print("test2")
            try:
                msg_ids = json.loads(ad.telegram_message_id)   # ✅ JSON korrekt laden
                if isinstance(msg_ids, str):
                    msg_ids = json.loads(msg_ids)
            except Exception as e:
                print("JSON parse error:", e)
                msg_ids = []
            print("test2")

            for msg_id in msg_ids:
                try:
                    await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg_id)
                except Exception as e:
                    print(f"⚠️ Telegram delete failed msg_id={msg_id}: {e}")

        print("test4")

        # --- DB löschen ---
        await session.execute(text("DELETE FROM ad_requests WHERE ad_id = :id"), {"id": ad_id})
        await session.execute(text("DELETE FROM ads WHERE id = :id"), {"id": ad_id})
        await session.commit()

    await query.edit_message_text("✅ Anzeige wurde komplett gelöscht (inkl. Kanal).")

# Handler hinzufügen
my_ads_handler = CommandHandler("show_my_ads", show_my_ads)
delete_ad_handler = CallbackQueryHandler(delete_ad_callback, pattern=r"delete_ad:\d+")
