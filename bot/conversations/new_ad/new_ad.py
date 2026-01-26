from enum import Enum, auto

from telegram import Update
from telegram.ext import ContextTypes
from .states import NewAdState

class NewAdState(Enum):
    TITLE = auto()
    TYPE = auto()       # kommt in Schritt 2
    PRICE = auto()      # später
    CONFIRM = auto()    # später



async def new_ad_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # sauberen Start erzwingen

    await update.message.reply_text(
        "📝 Neue Anzeige erstellen\n\n"
        "Bitte gib den *Titel* deiner Anzeige ein:",
        parse_mode="Markdown"
    )

    return NewAdState.TITLE

async def new_ad_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = update.message.text.strip()

    if len(title) < 5:
        await update.message.reply_text(
            "❌ Der Titel ist zu kurz.\n"
            "Bitte gib mindestens 5 Zeichen ein:"
        )
        return NewAdState.TITLE

    context.user_data["title"] = title

    await update.message.reply_text(
        f"✅ Titel gespeichert:\n*{title}*\n\n"
        "➡️ Nächster Schritt kommt gleich.",
        parse_mode="Markdown"
    )

    return NewAdState.TYPE  # noch leer, kommt als nächstes

