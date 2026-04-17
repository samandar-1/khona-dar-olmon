from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from db.controllers.ad_controller import get_ad, get_approved_ads
from db.controllers.ad_request_controller import reject_ad, get_pending, approve_ad
from db.models import Ad
from db.database import AsyncSessionLocal
from bot.strings import AdminText, GeneralText, MyAdsText
from bot import utils
from sqlalchemy import delete
import os
import json
from telegram import InputMediaPhoto
from config.config import Config
import logging
logger = logging.getLogger(__name__)

ADMIN_IDS = Config.ADMIN_IDS
CHANNEL_ID = Config.CHANNEL_ID
CHANNEL_USERNAME = Config.CHANNEL_USERNAME

# ---------------------------
# HELPERS
# ---------------------------
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
async def admin_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text(AdminText.NOT_ADMIN)
        return

    keyboard = [
        [InlineKeyboardButton("🕓 Request Management", callback_data="admin:pending")],
        [InlineKeyboardButton("✅ Approved Ads", callback_data="admin:approved")]
    ]

    await update.message.reply_text(
        "🔧 *Admin Dashboard*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ---------------------------
# PENDING ADS
# ---------------------------
# async def admin_pending_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#
#     if not is_admin(query.from_user.id):
#         await query.message.reply_text(AdminText.NOT_ADMIN)
#         return
#
#     await query.message.reply_text("🕓 Request Management:")
#     requests = await get_pending()
#     if not requests:
#         await query.message.reply_text("✅ Keine offenen Anfragen.")
#         return
#
#     for req in requests:
#         ad = await get_ad(req.ad_id)
#         if not ad:
#             continue
#
#         text = await utils.generate_ad_text(ad)
#         bilder = json.loads(ad.bilder) if ad.bilder else []
#
#         keyboard = [[
#             InlineKeyboardButton("✅ Freigeben", callback_data=f"approve:{ad.id}"),
#             InlineKeyboardButton("❌ Ablehnen", callback_data=f"reject:{ad.id}")
#         ]]
#         markup = InlineKeyboardMarkup(keyboard)
#
#         if bilder:
#             media = [
#                 InputMediaPhoto(
#                     file_id,
#                     caption=text if i == 0 else None,
#                     parse_mode="HTML"
#                 )
#                 for i, file_id in enumerate(bilder)
#             ]
#             await query.message.reply_media_group(media)
#             await query.message.reply_text("Aktion auswählen:", reply_markup=markup)
#         else:
#             await query.message.reply_text(text, parse_mode="HTML", reply_markup=markup)
async def admin_pending_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text(AdminText.NOT_ADMIN)
        return

    await query.message.reply_text("🕓 Request Management:")
    requests = await get_pending()

    if not requests:
        await query.message.reply_text("✅ Keine offenen Anfragen.")
        return

    for ad in requests:
        text = await utils.generate_ad_text(ad)
        bilder = json.loads(ad.bilder) if ad.bilder else []

        keyboard = [[
            InlineKeyboardButton("✅ Freigeben", callback_data=f"approve:{ad.id}"),
            InlineKeyboardButton("❌ Ablehnen", callback_data=f"reject:{ad.id}")
        ]]
        markup = InlineKeyboardMarkup(keyboard)

        if bilder:
            media = [
                InputMediaPhoto(
                    file_id,
                    caption=text if i == 0 else None,
                    parse_mode="HTML"
                )
                for i, file_id in enumerate(bilder)
            ]
            await query.message.reply_media_group(media)
            await query.message.reply_text("Aktion auswählen:", reply_markup=markup)
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=markup)

# ---------------------------
# APPROVED ADS
# ---------------------------
async def admin_approved_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text(AdminText.NOT_ADMIN)
        return

    await query.message.reply_text("✅ Approved Ads:")
    ads = await get_approved_ads()
    if not ads:
        await query.message.reply_text("ℹ️ Keine freigegebenen Anzeigen.")
        return

    for ad in ads:
        text = await utils.generate_ad_text(ad, incl_status=True)

        bilder = json.loads(ad.bilder) if ad.bilder else []

        keyboard = [[
            InlineKeyboardButton("🗑 Löschen", callback_data=f"delete:{ad.id}")
        ]]
        markup = InlineKeyboardMarkup(keyboard)

        if bilder:
            media = [
                InputMediaPhoto(
                    file_id,
                    caption=text if i == 0 else None,
                    parse_mode="HTML"
                )
                for i, file_id in enumerate(bilder)
            ]
            await query.message.reply_media_group(media)
            await query.message.reply_text("Aktion auswählen:", reply_markup=markup)
        else:
            await query.message.reply_text(text, parse_mode="HTML", reply_markup=markup)



# ---------------------------
# ACTION HANDLER
# ---------------------------
async def admin_action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.message.reply_text(AdminText.NOT_ADMIN)
        return

    action, ad_id = query.data.split(":")
    ad_id = int(ad_id)

    ad = await get_ad(ad_id)
    if not ad:
        await query.edit_message_text("❌ Anzeige existiert nicht.")
        return

    if action == "approve":

        text = await utils.generate_ad_text(ad)
        bilder = json.loads(ad.bilder) if ad.bilder else []

        if bilder:
            media = [
                InputMediaPhoto(
                    file_id,
                    caption=text if i == 0 else None,
                    parse_mode="HTML"
                )
                for i, file_id in enumerate(bilder)
            ]
            msgs = await context.bot.send_media_group(CHANNEL_ID, media)
            msg_ids = [m.message_id for m in msgs]
        else:
            msg = await context.bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
            msg_ids = [msg.message_id]

        await approve_ad(ad_id, msg_ids)

        link = f"https://t.me/{CHANNEL_USERNAME}/{msg_ids[0]}"
        await context.bot.send_message(
            ad.user.telegram_id,
            f"{AdminText.YOUR_AD_APPROVED}\n{link}"
        )

        await query.edit_message_text("✅ Anzeige freigegeben.")
        logger.info("Anzeige freigegeben | ad_id=%s | admin=%s", ad_id, query.from_user.id)


    elif action == "reject":
        await reject_ad(ad_id)

        desc = ad.title or ""
        short_desc = desc[:50]
        await context.bot.send_message(
            ad.user.telegram_id,
            AdminText.YOUR_AD_REJECTED.format(short_desc)
        )
        await query.edit_message_text("❌ Anzeige abgelehnt.")
        logger.info("Anzeige abgelehnt | ad_id=%s | admin=%s", ad_id, query.from_user.id)

    elif action == "delete":
        await reject_ad(ad_id)

        desc = ad.title or ""
        short_desc = desc[:50]
        await context.bot.send_message(
            ad.user.telegram_id,
            AdminText.YOUR_AD_REJECTED.format(short_desc)
        )

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
                    logger.info("Anzeige gelöscht | ad_id=%s | admin=%s", ad_id, query.from_user.id)

                except Exception as e:
                    print(f"⚠️ Telegram delete failed msg_id={msg_id}: {e}")
                    logger.error("Telegram delete fehlgeschlagen | msg_id=%s | error=%s", msg_id, e)
                    await query.edit_message_text(MyAdsText.ERROR_DELETE_MY_AD)

        await query.edit_message_text("🗑 Anzeige gelöscht.")

#
# # Admin bekommt neue AdRequests
# async def admin_check_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     tg_id = update.effective_user.id
#
#     # print("Ad ID: ", type(ADMIN_ID))
#     if tg_id not in ADMIN_IDS:
#         await update.message.reply_text(AdminText.NOT_ADMIN)
#         return
#
#     # Hol alle offenen AdRequests
#     requests = await get_pending()
#     if not requests:
#         await update.message.reply_text("✅ Keine neuen Anzeigen zur Freigabe.")
#         return
#
#     for req in requests:
#         ad = await get_ad(ad_id=req.ad_id)
#         if not ad:
#             continue
#         keyboard = [
#             [InlineKeyboardButton("✅ Freigeben", callback_data=f"approve:{ad.id}"),
#              InlineKeyboardButton("❌ Ablehnen", callback_data=f"reject:{ad.id}")]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         text = await utils.generate_ad_text(ad=ad)
#         bilder = json.loads(ad.bilder) if ad.bilder else []
#
#         msg = update.message or update.callback_query.message
#
#         if bilder:
#             # Bilder + Text als Caption beim ersten Bild
#             media = [
#                 InputMediaPhoto(file_id, caption=text if i == 0 else None, parse_mode="HTML")
#                 for i, file_id in enumerate(bilder)
#             ]
#             # MediaGroup an Admin senden
#             await msg.reply_media_group(media)
#             # Inline-Buttons in separater Nachricht
#             await msg.reply_text("Aktion auswählen:", reply_markup=reply_markup)
#         else:
#             # Nur Text
#             await update.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)
#
#
# async def admin_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#
#     user_id = query.from_user.id
#     if user_id not in ADMIN_IDS:
#         await query.message.reply_text(AdminText.NOT_ADMIN)
#         return
#
#     action, ad_id = query.data.split(":")
#     ad_id = int(ad_id)
#
#     # ✅ DB CALL
#     ad = await get_ad(ad_id)
#     if not ad:
#         await query.edit_message_text("❌ Anzeige existiert nicht")
#         return
#
#     if action == "approve":
#         text = await utils.generate_ad_text(ad=ad)
#
#         bilder = json.loads(ad.bilder) if ad.bilder else []
#
#         # ---- SEND TO CHANNEL ----
#         if bilder:
#             media = [
#                 InputMediaPhoto(file_id, caption=text if i == 0 else None, parse_mode="HTML")
#                 for i, file_id in enumerate(bilder)
#             ]
#             msgs = await context.bot.send_media_group(CHANNEL_ID, media)
#             msg_ids = [m.message_id for m in msgs]
#         else:
#             msg = await context.bot.send_message(CHANNEL_ID, text, parse_mode="HTML")
#             msg_ids = [msg.message_id]
#
#         # ✅ DB UPDATE
#         await approve_ad(ad_id, msg_ids)
#
#         link = f"https://t.me/{CHANNEL_USERNAME}/{msg_ids[0]}"
#
#         await context.bot.send_message(ad.user.telegram_id, f"{AdminText.YOUR_AD_APPROVED} {link}")
#         await query.edit_message_text("✅ Freigegeben")
#
#     elif action == "reject":
#         await reject_ad(ad_id)
#         # await context.bot.send_message(ad.user_id, f"❌ Deine Anzeige '{ad.title}' wurde abgelehnt")
#         await context.bot.send_message(ad.user.telegram_id, f"❌ Deine Anzeige '{ad.title}' wurde abgelehnt")
#         await context.bot.send_message(ad.user.telegram_id, AdminText.YOUR_AD_REJECTED.format(ad.title))
#         await query.edit_message_text("❌ Abgelehnt")
#
