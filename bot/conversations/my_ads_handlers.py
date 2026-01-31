from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from db.controllers.ad_controller import get_user_ads, get_ad, delete_ad, get_user_id_by_telegram
import json, os
from dotenv import load_dotenv
from bot.strings import MyAdsText, GeneralText
from bot import utils

load_dotenv()
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# /show_my_ads Command
async def show_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    user_id = await get_user_id_by_telegram(tg_id)
    ads = await get_user_ads(user_id)
    print("userid", user_id)
    if not ads:
        await update.message.reply_text(MyAdsText.NO_ADS_YET)
        return

    for ad in ads:
        reply_text = await utils.generate_ad_text(ad=ad, incl_status=True)

        keyboard = [[InlineKeyboardButton(MyAdsText.DELETE_MY_AD_BUTTON, callback_data=f"delete_ad:{ad.id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bilder = json.loads(ad.bilder) if ad.bilder else []
        if bilder:
            # Text als Caption nur beim ersten Bild
            media = [
                # InputMediaPhoto(file_id, parse_mode="HTML", caption=reply_text if i == 0 else None)
                InputMediaPhoto(file_id, parse_mode="HTML")
                for i, file_id in enumerate(bilder)
            ]
            await update.message.reply_media_group(media)
            # await update.message.reply_text(MyAdsText.ACTION, reply_markup=reply_markup)
            await update.message.reply_text(reply_text, parse_mode="HTML", reply_markup=reply_markup)
        else:
            await update.message.reply_text(reply_text, parse_mode="HTML", reply_markup=reply_markup)

# Callback für Löschen
async def delete_ad_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ad_id = int(query.data.split(":")[1])
    tg_id = query.from_user.id
    user_id = await get_user_id_by_telegram(tg_id)

    print("userid::", user_id)
    print("tg::", tg_id)
    ad = await get_ad(ad_id)
    if not ad or ad.user_id != user_id:
        await query.edit_message_text(MyAdsText.GET_AD_ERROR)
        return
    print("test1")
    # Telegram Nachrichten löschen
    if ad.telegram_message_id:
        print("test2")

        try:
            msg_ids = json.loads(ad.telegram_message_id)
            if isinstance(msg_ids, str):
                print("test3")
                msg_ids = json.loads(msg_ids)
        except Exception:
            msg_ids = []

        for msg_id in msg_ids:
            try:
                print("test4")
                await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg_id)
            except Exception as e:
                print(f"⚠️ Telegram delete failed msg_id={msg_id}: {e}")
                await query.edit_message_text(MyAdsText.ERROR_DELETE_MY_AD)


    # DB löschen
    await delete_ad(ad_id)
    await query.edit_message_text(MyAdsText.AD_DELETED)

# Handler
my_ads_handler = CommandHandler("show_my_ads", show_my_ads)
delete_ad_handler = CallbackQueryHandler(delete_ad_callback, pattern=r"^delete_ad:\d+$")
