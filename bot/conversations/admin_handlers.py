from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from db.controllers.ad_controller import get_ad
from db.controllers.ad_request_controller import reject_ad, get_pending, approve_ad
from db.models import AdRequest, Ad
from sqlalchemy import delete
from db.database import AsyncSessionLocal
from dotenv import load_dotenv
import os
import json
from telegram import InputMediaPhoto

load_dotenv()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x] # deine Telegram-User-ID(s)
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))


# Admin bekommt neue AdRequests
async def admin_check_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # print("Ad ID: ", type(ADMIN_ID))
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Du bist kein Admin!")
        return

    # Hol alle offenen AdRequests
    requests = await get_pending()
    if not requests:
        await update.message.reply_text("✅ Keine neuen Anzeigen zur Freigabe.")
        return

    for req in requests:
        ad = await get_ad(ad_id=req.ad_id)
        if not ad:
            continue
        keyboard = [
            [InlineKeyboardButton("✅ Freigeben", callback_data=f"approve:{ad.id}"),
             InlineKeyboardButton("❌ Ablehnen", callback_data=f"reject:{ad.id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = (
            f"*{ad.title}*\n"
            f"{ad.vermietung_art}, {ad.type}\n"
            f"{ad.raumflaeche} m², {ad.stadt}\n"
            f"Kaltmiete: {ad.kaltmiete}, Nebenkosten: {ad.nebenkosten}\n"
            f"Start: {ad.start_date}, Ende: {ad.end_date}\n"
        )
        bilder = json.loads(ad.bilder) if ad.bilder else []

        if bilder:
            # Bilder + Text als Caption beim ersten Bild
            media = [
                InputMediaPhoto(file_id, caption=text if i == 0 else None, parse_mode="Markdown")
                for i, file_id in enumerate(bilder)
            ]
            # MediaGroup an Admin senden
            await update.message.reply_media_group(media)
            # Inline-Buttons in separater Nachricht
            await update.message.reply_text("Aktion auswählen:", reply_markup=reply_markup)
        else:
            # Nur Text
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)


async def admin_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        await query.message.reply_text("❌ Kein Admin")
        return

    action, ad_id = query.data.split(":")
    ad_id = int(ad_id)

    # ✅ DB CALL
    ad = await get_ad(ad_id)
    if not ad:
        await query.edit_message_text("❌ Anzeige existiert nicht")
        return

    if action == "approve":
        text = f"""
            <b>{ad.title}</b>
            {ad.vermietung_art}, {ad.type}
            {ad.raumflaeche} m², {ad.stadt}
            Kaltmiete: {ad.kaltmiete}, NK: {ad.nebenkosten}
            Start: {ad.start_date}, Ende: {ad.end_date}
            
            <a href="tg://user?id={ad.user_id}">Kontakt</a>
            """

        bilder = json.loads(ad.bilder) if ad.bilder else []
        msg_ids = []

        # ---- SEND TO CHANNEL ----
        if bilder:
            media = [
                InputMediaPhoto(file_id, caption=text if i == 0 else None, parse_mode="HTML")
                for i, file_id in enumerate(bilder)
            ]
            msgs = await context.bot.send_media_group(CHANNEL_ID, media)
            msg_ids = [m.message_id for m in msgs]
        else:
            msg = await context.bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
            msg_ids = [msg.message_id]

        # ✅ DB UPDATE
        await approve_ad(ad_id, msg_ids)

        link = f"https://t.me/{CHANNEL_USERNAME}/{msg_ids[0]}"
        await context.bot.send_message(ad.user_id, f"✅ Deine Anzeige wurde freigegeben!\n🔗 {link}")
        await query.edit_message_text("✅ Freigegeben")

    elif action == "reject":
        await reject_ad(ad_id)
        await context.bot.send_message(ad.user_id, f"❌ Anzeige '{ad.title}' wurde abgelehnt")
        await query.edit_message_text("❌ Abgelehnt")

