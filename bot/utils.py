from bot.strings import GeneralText, NewAdText
# from telegram.helpers import escape_markdown
from html import escape
import os
from bot import utils
from dotenv import load_dotenv

load_dotenv()
CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))


async def telegram_message_exists(bot, chat_id, message_id):
    try:
        await bot.copy_message(
            chat_id=chat_id,
            from_chat_id=chat_id,
            message_id=message_id
        )
        return True
    except Exception:
        return False


def get_contact_text(user):
    name = (user.first_name or "") + " " + (user.last_name or "")
    name = name.strip() or GeneralText.UNKNOWN

    if user.username:
        return escape(f"@{user.username} ({name})")
    else:
        return escape(name)


def bool_to_text(val):
    return escape(f"{NewAdText.ANMELDUNG_YES}" if val else f"{NewAdText.ANMELDUNG_NO}")

def hashtag_last_word(text: str) -> str:
    parts = text.strip().split()

    if not parts:
        return text  # leerer String

    parts[-1] = f"#{parts[-1]}"
    return " ".join(parts)


async def generate_ad_text(ad, incl_status=False):
    contact_name = get_contact_text(ad.user)

    text = f"""
<b>{escape(hashtag_last_word(ad.vermietung_art))} | {escape(hashtag_last_word(ad.type.upper()))}</b>

<b>{escape(GeneralText.STADT)}:</b> #{escape(ad.stadt) or '-'}
<b>{escape(GeneralText.FLAECHE)}:</b> {escape(ad.raumflaeche) or '-'} m²

<b>{escape(GeneralText.KALTMIETE)}:</b> {escape(ad.kaltmiete) or '-'} €
<b>{escape(GeneralText.NEBENKOSTEN)}:</b> {escape(ad.nebenkosten) or '-'}

<b>{escape(GeneralText.START)}:</b> {escape(ad.start_date) or '-'}
<b>{escape(GeneralText.ENDE)}:</b> {escape(ad.end_date) or '-'}
<b>{escape(GeneralText.ANMELDUNG)}:</b> {bool_to_text(ad.anmeldung_moeglich)}
           --------------------
<b>{escape(GeneralText.BESCHREIBUNG)}:</b>
{escape(ad.title)}

<b>{escape(GeneralText.KONTAKT)}:</b> {escape(contact_name)}
<a href="tg://user?id={ad.user.telegram_id}">{escape(GeneralText.DIREKT_ANSCHREIBEN)}</a>
           """
    if incl_status:
        if ad.approved:
            text += escape(f"\n\n✅ {GeneralText.STATUS}: {GeneralText.STATUS_APPROVED}")
            link = f"https://t.me/{CHANNEL_USERNAME}/{ad.telegram_message_id[0]}"
            text += escape(f"🔗Link: {link}")
        else:
            text += escape(f"\n\n⏳ {GeneralText.STATUS}: {GeneralText.STATUS_PENDING}")
    return text
