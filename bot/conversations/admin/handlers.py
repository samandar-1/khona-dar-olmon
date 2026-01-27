from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from db.controllers.ad_controller import approve_ad, reject_ad, get_ad_by_id
from db.controllers.ad_request_controller import get_pending
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
        ad = await get_ad_by_id(ad_id=req.ad_id)
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
        print(text)
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

    async with AsyncSessionLocal() as session:
        ad = await session.get(Ad, ad_id)

        if action == "approve":
            ad.approved = True

            text = f"""
                <b>{ad.title}</b>
                {ad.vermietung_art}, {ad.type}
                {ad.raumflaeche} m², {ad.stadt}
                Kaltmiete: {ad.kaltmiete}, NK: {ad.nebenkosten}
                Start: {ad.start_date}, Ende: {ad.end_date}
                
                
                <a href="tg://user?id={ad.user_id}">Kontakt</a> 
                """
            # if ad.user.first_name:


            bilder = json.loads(ad.bilder) if ad.bilder else []

            text_msg = await context.bot.send_message(CHANNEL_ID, text, parse_mode="HTML")

            msg_ids = [text_msg.message_id]

            if bilder:
                media = [InputMediaPhoto(file_id) for file_id in bilder]
                bilder_msgs = await context.bot.send_media_group(CHANNEL_ID, media)
                msg_ids.extend(m.message_id for m in bilder_msgs)

            ad.telegram_message_id = json.dumps(msg_ids)
            await session.commit()

            link = f"https://t.me/{CHANNEL_USERNAME}/{text_msg.message_id}"

            await context.bot.send_message(
                ad.user_id,
                f"✅ Deine Anzeige wurde freigegeben!\n🔗 {link}"
            )

            await query.edit_message_text("✅ Freigegeben")

        elif action == "reject":


            await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))
            await session.execute(delete(Ad).where(Ad.id == ad_id))
            await session.commit()

            await context.bot.send_message(ad.user_id, f"❌ Anzeige '{ad.title}' wurde abgelehnt")
            await query.edit_message_text("❌ Abgelehnt")
