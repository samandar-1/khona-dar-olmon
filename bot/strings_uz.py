class GeneralText:
    COMMAND_NEW_AD = "➕ Yangi e'lon"
    COMMAND_SHOW_MY_ADS = "📋 Mening e'lonlarim"
    COMMAND_ADMIN_ADS = "🛠 Admin tekshiruvi"

    # Umumiy e'lon ma'lumotlari
    UNKNOWN = "❓ Noma'lum"
    STADT = "📍 Shahar"
    FLAECHE = "📐 Maydon"
    KALTMIETE = "💰 Ijara (Kaltmiete)"
    NEBENKOSTEN = "💸 Qo‘shimcha xarajatlar"
    START = "➡️ Ko‘chish mumkin bo‘lgan sana"
    ENDE = "⬅️ Tugash sanasi"
    ANMELDUNG = "📝 Propiska (Anmeldung)"
    BESCHREIBUNG = "🧾 E'lon tavsifi"
    KONTAKT = "📞 Aloqa"
    DIREKT_ANSCHREIBEN = "👉 Shaxsiyga yozish"
    STATUS = "Status"
    STATUS_APPROVED = "Kanaldа chop etildi"
    STATUS_PENDING = "Tekshiruvda"

    AD_CREATE_TIME = "Elon sanasi"
    SUBSCRIBE_INFO = "❗ Botdan foydalanish uchun avval kanalga obuna bo‘ling."
    SUBSCRIBE_TO_CHANNEL = "📢 Kanalga obuna bo‘lish"
    SUBSCRIBED_TO_CHANNEL = "✅ Obuna bo‘ldim"

    THANKS_FOR_SUBSCRIPTION = "✅ Rahmat! Endi /new_ad dan foydalanishingiz mumkin."
    STILL_NOT_SUBSCRIBED = "❌ Siz hali obuna emassiz. Iltimos, kanalga obuna bo‘ling."


class AdminText:
    NOT_ADMIN = "❌ Siz admin emassiz!"

    YOUR_AD_APPROVED = "✅ E'loningiz tasdiqlandi!\n🔗"
    YOUR_AD_REJECTED = "❌ E'loningiz «{}» rad etildi."
    YOUR_AD_DELETED = "❌ E'loningiz «{}» o‘chirildi."


class MyAdsText:
    NO_ADS_YET = "📭 Sizda hali e'lonlar yo‘q."
    DELETE_MY_AD_BUTTON = "🗑 O‘chirish"
    ACTION = "⚙ Amal:"
    GET_AD_ERROR = "❌ Ruxsat yo‘q yoki e'lon topilmadi."
    ERROR_DELETE_MY_AD = "❌ E'lonni o‘chirishda xatolik."
    AD_DELETED = "✅ E'lon to‘liq o‘chirildi (kanaldan ham)."


class NewAdText:
    SELECT_VERMIETUNG_ART = (
        "📝 Yangi e'lon berish.\n"
        "🏠 Ijara turini tanlang:"
    )

    VERMIETUNG_ART_WG = "🚪Xona (WG)"
    VERMIETUNG_ART_WOHNUNG = "🏢 Kvartira"
    VERMIETUNG_ART_HAUS = "🏡 Uy"
    VERMIETUNG_ART_PARKPLATZ = "🅿 Avtoturargoh"

    SELECTED_VERMIETUNG_ART = "✅ Tanlangan ijara turi:"

    SELECT_AD_TYPE = "📢 E'lon turini tanlang:"
    AD_TYPE_GESUCH = "🔴 Qidiryapman"
    AD_TYPE_ANGEBOT = "🟢 Taklif"
    SELECTED_AD_TYPE = "✅ Tanlangan e'lon turi:"

    INPUT_CITY = "🏙 Shahar nomini kiriting:"

    INPUT_KALTMIETE = "💶 Ijara narxi (Kaltmiete €):"
    ERROR_INPUT_KALTMIETE = "❌ Xato kiritildi. Faqat raqam yozing."

    INPUT_NEBENKOSTEN = "💸 Qo‘shimcha xarajatlar (€):"

    INPUT_RAUMFLAECHE = "📐 Maydon (m²)\n(Agar noma'lum bo‘lsa '-' yozing):"

    SELECT_ANMELDUNG = "📝 Propiska (Anmeldung) mumkinmi?"
    ANMELDUNG_YES = "✅ Ha"
    ANMELDUNG_NO = "❌ Yo‘q"
    SELECTED_ANMELDUNG = "✅ Propiska:"

    INPUT_START_DATE = "📅 Qachondan?\n(Agar noma'lum bo‘lsa '-' yozing)"
    INPUT_END_DATE = "📅 Qachongacha?\n(Agar noma'lum bo‘lsa '-' yozing)"

    INPUT_BESCHREIBUNG = "🧾 E'lon tavsifini yozing:"
    ERROR_BESCHREIBUNG = "❌ Tavsif juda qisqa (kamida 5 ta harf)."

    READY_ADD_PHOTO = (
        "✅ Barcha ma'lumotlar kiritildi!\n"
        "📷 Ixtiyoriy: rasm yuboring\n"
        "➡️ Tugatish uchun /finish ni bosing."
    )
    ADDED_PHOTO = (
        "✅ Rasm qo‘shildi (jami {}).\n"
        "➡️ Tugatish uchun /finish ni bosing."
    )
    ERROR_ADD_PHOTO = "❌ Rasm topilmadi. Yana urinib ko‘ring."

    AD_SAVED = "✅ E'lon saqlandi! ⏳ Admin tekshiradi."

    AD_LIMIT_REACHED = (
        "❌ Siz maksimal {} ta e'longa yetdingiz.\n\n"
        "🗑 Avval bittasini o‘chiring."
    )