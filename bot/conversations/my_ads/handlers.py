from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db.database import AsyncSessionLocal
from db.controllers.ad_controller import get_ad_by_id
from db.models import Ad
import asyncio
from sqlalchemy import text

# /my_ads Command
async def show_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(
            "SELECT id, title, type, approved FROM ads WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        ads = result.fetchall()

    if not ads:
        await update.message.reply_text("Du hast noch keine Anzeigen.")
        return

    for ad in ads:
        ad_id, title, ad_type, approved = ad
        keyboard = [
            [InlineKeyboardButton("Löschen ❌", callback_data=f"delete_ad:{ad_id}")]
        ]
        status = "in Prüfung"
        if approved:
            status = "im Kanal veröffentlicht"
        await update.message.reply_text(
            f"ID: {ad_id}\nBeschreibung: {title}\nTyp: {ad_type}\nStatus: {status}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# Callback für Löschen
import json
from sqlalchemy import text

async def delete_my_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ad_id = int(query.data.split(":")[1])
    user_id = query.from_user.id

    async with AsyncSessionLocal() as session:

        # --- Anzeige holen ---
        ad = await session.get(Ad, ad_id)
        if not ad or ad.user_id != user_id:
            await query.edit_message_text("❌ Keine Berechtigung oder Anzeige existiert nicht.")
            return

        # --- Telegram Channel Messages löschen ---
        if ad.telegram_message_id:
            try:
                msg_ids = json.loads(ad.telegram_message_id)   # ✅ JSON korrekt laden
            except Exception as e:
                print("JSON parse error:", e)
                msg_ids = []

            for msg_id in msg_ids:
                try:
                    await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg_id)
                except Exception as e:
                    print(f"⚠️ Telegram delete failed msg_id={msg_id}: {e}")

        # --- DB löschen ---
        await session.execute(text("DELETE FROM ad_requests WHERE ad_id = :id"), {"id": ad_id})
        await session.execute(text("DELETE FROM ads WHERE id = :id"), {"id": ad_id})
        await session.commit()

    await query.edit_message_text("✅ Anzeige wurde komplett gelöscht (inkl. Kanal).")

# Handler hinzufügen
my_ads_handler = CommandHandler("show_my_ads", show_my_ads)
delete_ad_handler = CallbackQueryHandler(delete_ad_callback, pattern=r"delete_ad:\d+")
