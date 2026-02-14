import json
from telegram.ext import ConversationHandler
from db.database import AsyncSessionLocal
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from .states import NewAdState, MAX_ADS_PER_USER
from db.controllers.ad_controller import create_ad  # unsere DB-Funktion
from db.controllers.ad_request_controller import create_ad_request
from db.controllers.user_controller import save_or_update_user
from db.controllers.ad_controller import get_user_ads, get_user_id_by_telegram, count_user_ads
from db.models import AdRequest
from bot.utils import bool_to_text, is_user_subscribed
from bot.strings import GeneralText, NewAdText
import os
from dotenv import load_dotenv


load_dotenv()
CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))


# Schritt 1: /new_ad starten
async def new_ad_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    subscribed = await is_user_subscribed(context.bot, tg_id)
    if not subscribed:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(GeneralText.SUBSCRIBE_TO_CHANNEL, url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton(GeneralText.SUBSCRIBED_TO_CHANNEL, callback_data="check_sub")]
        ])

        await update.message.reply_text(
            GeneralText.SUBSCRIBE_INFO,
            reply_markup=keyboard
        )
        return ConversationHandler.END

    user_id = await get_user_id_by_telegram(tg_id)

    ads_count = await count_user_ads(user_id)

    if ads_count >= MAX_ADS_PER_USER:
        await update.message.reply_text(NewAdText.AD_LIMIT_REACHED.format(MAX_ADS_PER_USER))
        return ConversationHandler.END

    context.user_data.clear()

    keyboard = [
        [InlineKeyboardButton(f"{NewAdText.VERMIETUNG_ART_WG}", callback_data=NewAdText.VERMIETUNG_ART_WG),
         InlineKeyboardButton(f"{NewAdText.VERMIETUNG_ART_WOHNUNG}", callback_data=NewAdText.VERMIETUNG_ART_WOHNUNG)],
        [InlineKeyboardButton(f"{NewAdText.VERMIETUNG_ART_HAUS}", callback_data=NewAdText.VERMIETUNG_ART_HAUS),
         InlineKeyboardButton(f"{NewAdText.VERMIETUNG_ART_PARKPLATZ}", callback_data=NewAdText.VERMIETUNG_ART_PARKPLATZ)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(NewAdText.SELECT_VERMIETUNG_ART, reply_markup=reply_markup)
    return NewAdState.VERMIETUNG_ART


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    if await is_user_subscribed(context.bot, user_id):
        await query.message.reply_text(GeneralText.THANKS_FOR_SUBSCRIPTION)
    else:
        await query.message.reply_text(GeneralText.STILL_NOT_SUBSCRIBED)


async def new_ad_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["vermietung_art"] = query.data
    await query.edit_message_text(f"{NewAdText.SELECTED_VERMIETUNG_ART}: {query.data}")
    # Nächster Schritt: Anzeige-Typ
    return await new_ad_type_choice(update, context)


# Schritt 3: Anzeige-Typ auswählen (Gesuch/Angebot)
async def new_ad_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{NewAdText.AD_TYPE_GESUCH}", callback_data=NewAdText.AD_TYPE_GESUCH),
         InlineKeyboardButton(f"{NewAdText.AD_TYPE_ANGEBOT}", callback_data=NewAdText.AD_TYPE_ANGEBOT)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        NewAdText.SELECT_AD_TYPE, reply_markup=reply_markup
    )
    return NewAdState.AD_TYPE


async def new_ad_type_callback2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["type"] = query.data
    await query.edit_message_text(f"{NewAdText.SELECTED_AD_TYPE} {query.data}")
    await query.message.reply_text(NewAdText.INPUT_CITY)
    return NewAdState.STADT


# Stadt
async def new_ad_stadt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["stadt"] = update.message.text.strip()

    await update.message.reply_text(NewAdText.INPUT_KALTMIETE)
    return NewAdState.KALTMIETE


# Kaltmiete
async def new_ad_kaltmiete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        try:
            context.user_data["kaltmiete"] = float(text.replace(",", "."))
        except ValueError:
            await update.message.reply_text(NewAdText.ERROR_INPUT_KALTMIETE)
            return NewAdState.KALTMIETE
    else:
        context.user_data["kaltmiete"] = None
    await update.message.reply_text(NewAdText.INPUT_NEBENKOSTEN)
    return NewAdState.NEBENKOSTEN


# Nebenkosten
async def new_ad_nebenkosten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        context.user_data["nebenkosten"] = text
    else:
        context.user_data["nebenkosten"] = None
    await update.message.reply_text(NewAdText.INPUT_RAUMFLAECHE)
    return NewAdState.RAUMFLAECHE


# Raumfläche
async def new_ad_raumflaeche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text:
        context.user_data["raumflaeche"] = text
        # return NewAdState.RAUMFLAECHE
    else:
        context.user_data["raumflaeche"] = None
    keyboard = [
        [InlineKeyboardButton(NewAdText.ANMELDUNG_YES, callback_data="True"),
         InlineKeyboardButton(NewAdText.ANMELDUNG_NO, callback_data="False")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(NewAdText.SELECT_ANMELDUNG, reply_markup=reply_markup)
    return NewAdState.ANMELDUNG


# Anmeldung
async def new_ad_anmeldung_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["anmeldung_moeglich"] = query.data == "True"
    await query.edit_message_text(f"{NewAdText.SELECTED_ANMELDUNG} {bool_to_text(context.user_data['anmeldung_moeglich'])}")
    await query.message.reply_text(NewAdText.INPUT_START_DATE)
    return NewAdState.START_DATE


# Startdatum
async def new_ad_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        context.user_data["start_date"] = text

        # return NewAdState.START_DATE
    await update.message.reply_text(NewAdText.INPUT_END_DATE)
    return NewAdState.END_DATE


# Enddatum
async def new_ad_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        context.user_data["end_date"] = text
        # return NewAdState.END_DATE

    else:
        context.user_data["end_date"] = None

    await update.message.reply_text(NewAdText.INPUT_BESCHREIBUNG)
    return NewAdState.TITLE


async def new_ad_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text.strip()
    if len(title) < 5:
        await update.message.reply_text(NewAdText.ERROR_BESCHREIBUNG)
        return NewAdState.TITLE
    context.user_data["title"] = title

    # Weiter
    await update.message.reply_text(NewAdText.READY_ADD_PHOTO)
    return NewAdState.BILDER


# Bilder sammeln
async def new_ad_bilder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not "bilder" in context.user_data:
        context.user_data["bilder"] = []

    photos = update.message.photo
    if photos:
        file_id = photos[-1].file_id  # höchste Auflösung
        context.user_data["bilder"].append(file_id)
        await update.message.reply_text(NewAdText.ADDED_PHOTO.format(len(context.user_data["bilder"])))
    else:
        await update.message.reply_text(NewAdText.ERROR_ADD_PHOTO)

    return NewAdState.BILDER


# Anzeige abschließen
async def new_ad_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    data = context.user_data.copy()

    # Save user
    user = await save_or_update_user(tg_user)

    # Save ad
    ad = await create_ad(
        user_id=user.id,
        title=data["title"],
        vermietung_art=data["vermietung_art"],
        type=data["type"],
        kaltmiete=data.get("kaltmiete"),
        nebenkosten=data.get("nebenkosten"),
        raumflaeche=data.get("raumflaeche"),
        stadt=data.get("stadt"),
        anmeldung_moeglich=data.get("anmeldung_moeglich"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        bilder=json.dumps(data.get("bilder", [])),
        approved=False
    )

    # Create request
    await create_ad_request(user_id=user.id, ad_id=ad.id, action="create")

    await update.message.reply_text(NewAdText.AD_SAVED)
    context.user_data.clear()
    return ConversationHandler.END
