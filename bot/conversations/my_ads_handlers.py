from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db.controllers.ad_controller import get_user_ads, get_ad, delete_ad
import json, os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# /show_my_ads Command
async def show_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ads = await get_user_ads(user_id)

    if not ads:
        await update.message.reply_text("Du hast noch keine Anzeigen.")
        return

    for ad in ads:
        reply_text = (
            f"🆔 ID: {ad.id}\n"
            f"📄 Beschreibung: {ad.title}\n"
            f"🏷 Typ: {ad.type}\n"
        )
        reply_text += "✅ Status: im Kanal veröffentlicht\n" if ad.approved else "⏳ Status: in Prüfung\n"

        keyboard = [[InlineKeyboardButton("Löschen ❌", callback_data=f"delete_ad:{ad.id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bilder = json.loads(ad.bilder) if ad.bilder else []
        msg_ids = json.loads(ad.telegram_message_id) if ad.telegram_message_id else []

        if bilder:
            # Text als Caption nur beim ersten Bild
            media = [
                InputMediaPhoto(file_id, caption=reply_text if i == 0 else None)
                for i, file_id in enumerate(bilder)
            ]
            await update.message.reply_media_group(media)
            await update.message.reply_text("Aktion:", reply_markup=reply_markup)
        else:
            await update.message.reply_text(reply_text, reply_markup=reply_markup)

# Callback für Löschen
async def delete_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ad_id = int(query.data.split(":")[1])
    user_id = query.from_user.id

    ad = await get_ad(ad_id)
    if not ad or ad.user_id != user_id:
        await query.edit_message_text("❌ Keine Berechtigung oder Anzeige existiert nicht.")
        return

    # Telegram Nachrichten löschen
    if ad.telegram_message_id:
        try:
            msg_ids = json.loads(ad.telegram_message_id)
            if isinstance(msg_ids, str):
                msg_ids = json.loads(msg_ids)
        except Exception:
            msg_ids = []

        for msg_id in msg_ids:
            try:
                await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg_id)
            except Exception as e:
                print(f"⚠️ Telegram delete failed msg_id={msg_id}: {e}")

    # DB löschen
    await delete_ad(ad_id)
    await query.edit_message_text("✅ Anzeige wurde komplett gelöscht (inkl. Kanal).")

# Handler
my_ads_handler = CommandHandler("show_my_ads", show_my_ads)
delete_ad_handler = CallbackQueryHandler(delete_ad_callback, pattern=r"^delete_ad:\d+$")
