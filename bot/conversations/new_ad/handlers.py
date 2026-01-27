import json
from telegram.ext import ConversationHandler
from db.database import AsyncSessionLocal
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from .states import NewAdState
from .new_ad import save_or_update_user
from db.controllers.ad_controller import create_ad # unsere DB-Funktion
from db.controllers import ad_request_controller
from db.models import AdRequest

# Schritt 1: /new_ad starten
async def new_ad_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [
        [InlineKeyboardButton("WG", callback_data="WG"),
         InlineKeyboardButton("Wohnung", callback_data="Wohnung")],
        [InlineKeyboardButton("Haus", callback_data="Haus"),
         InlineKeyboardButton("Parkplatz", callback_data="Parkplatz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📝 Neue Anzeige erstellen\n🏠 Wähle die Art der Vermietung:", reply_markup=reply_markup)
    return NewAdState.VERMIETUNG_ART


# Schritt 2: Vermietungsart (WG/Wohnung/Haus/Parkplatz)
# async def new_ad_type_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("WG", callback_data="WG"),
#          InlineKeyboardButton("Wohnung", callback_data="Wohnung")],
#         [InlineKeyboardButton("Haus", callback_data="Haus"),
#          InlineKeyboardButton("Parkplatz", callback_data="Parkplatz")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("🏠 Wähle die Art der Vermietung:", reply_markup=reply_markup)
#     return NewAdState.VERMIETUNG_ART

async def new_ad_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["vermietung_art"] = query.data
    await query.edit_message_text(f"✅ Vermietungsart: {query.data}")
    # Nächster Schritt: Anzeige-Typ
    return await new_ad_type_choice(update, context)

# Schritt 3: Anzeige-Typ auswählen (Gesuch/Angebot)
async def new_ad_type_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Gesuch", callback_data="gesucht"),
         InlineKeyboardButton("Angebot", callback_data="angebot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "Bitte wähle den Typ der Anzeige:", reply_markup=reply_markup
    )
    return NewAdState.AD_TYPE

async def new_ad_type_callback2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["type"] = query.data
    await query.edit_message_text(f"✅ Anzeige-Typ: {query.data}")
    await query.message.reply_text("🏙 Stadt eingeben:")
    return NewAdState.STADT


# Stadt
async def new_ad_stadt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["stadt"] = update.message.text.strip()

    await update.message.reply_text("💰 Gib bitte die Kaltmiete ein (€):")
    return NewAdState.KALTMIETE




# Kaltmiete
async def new_ad_kaltmiete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        try:
            context.user_data["kaltmiete"] = float(text.replace(",", "."))
        except ValueError:
            await update.message.reply_text("❌ Ungültige Zahl, bitte nur Zahlen eingeben:")
            return NewAdState.KALTMIETE
    else:
        context.user_data["kaltmiete"] = None
    await update.message.reply_text("💰 Gib bitte die Nebenkosten ein (€):")
    return NewAdState.NEBENKOSTEN

# Nebenkosten
async def new_ad_nebenkosten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:

        context.user_data["nebenkosten"] = text
        # return NewAdState.NEBENKOSTEN

    else:
        context.user_data["nebenkosten"] = None
    await update.message.reply_text("📐 Raumfläche (m²) eingeben:")
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
        [InlineKeyboardButton("Ja", callback_data="True"),
         InlineKeyboardButton("Nein", callback_data="False")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📝 Anmeldung möglich?", reply_markup=reply_markup)
    return NewAdState.ANMELDUNG

# Anmeldung
async def new_ad_anmeldung_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["anmeldung_moeglich"] = query.data == "True"
    await query.edit_message_text(f"✅ Anmeldung möglich: {context.user_data['anmeldung_moeglich']}")
    await query.message.reply_text("📅 Ab wann? (TT.MM.JJJJ)")
    return NewAdState.START_DATE

# Startdatum
async def new_ad_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        context.user_data["start_date"] = text

        # return NewAdState.START_DATE
    await update.message.reply_text("📅 Bis wann? „-“ eingeben, wenn offen")
    return NewAdState.END_DATE

# Enddatum
async def new_ad_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text:
        context.user_data["end_date"] = text
        # return NewAdState.END_DATE

    else:
        context.user_data["end_date"] = None

    await update.message.reply_text("Bitte gib Beschreibung deiner Anzeige ein:")
    return NewAdState.TITLE

async def new_ad_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text.strip()
    if len(title) < 5:
        await update.message.reply_text("❌ Beschreibung zu kurz, bitte mindestens 5 Zeichen.")
        return NewAdState.TITLE
    context.user_data["title"] = title
    # Weiter
    await update.message.reply_text(
        "✅ Alle Daten gesammelt! Optional: Bilder senden oder//und /finish eingeben, um Anzeige zu speichern."
    )
    return NewAdState.BILDER



# Bilder sammeln
async def new_ad_bilder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not "bilder" in context.user_data:
        context.user_data["bilder"] = []

    photos = update.message.photo
    if photos:
        file_id = photos[-1].file_id  # höchste Auflösung
        context.user_data["bilder"].append(file_id)
        await update.message.reply_text(f"✅ Bild hinzugefügt ({len(context.user_data['bilder'])} insgesamt). Jetzt /finish eingeben, um Anzeige zu speichern.")
    else:
        await update.message.reply_text("❌ Kein Bild erkannt.")

    return NewAdState.BILDER

# Anzeige abschließen
async def new_ad_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    user_id = tg_user.id
    data = context.user_data.copy()

    # ✅ User speichern / updaten
    async with AsyncSessionLocal() as session:
        user = await save_or_update_user(session, update.effective_user)
        print(user.id, user.username)

    # DB speichern
    ad = await create_ad(
        user_id=user_id,
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
        approved=False  # wird vom Admin freigegeben

    )

    # AdRequest für Admin-Freigabe erstellen
    await ad_request_controller.create_ad_request(user_id=user_id, ad_id=ad.id, action="create")



    await update.message.reply_text("✅ Anzeige gespeichert! Admin wird sie prüfen und freigeben.")
    context.user_data.clear()
    return ConversationHandler.END

async def back_to_ad_type(update, context):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "Wähle erneut Gesuch oder Angebot:"
    )

    return NewAdState.AD_TYPE




