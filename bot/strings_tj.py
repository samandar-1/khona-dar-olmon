class GeneralText:
    COMMAND_NEW_AD = "➕ Эълони нав"
    COMMAND_SHOW_MY_ADS = "📋 Эълонҳои ман"
    COMMAND_ADMIN_ADS = "🛠 Санҷиши админ"

    # Allgemeine Anzeigen-Labels
    UNKNOWN = "❓ Номаълум"
    STADT = "📍 Шаҳр"
    FLAECHE = "📐 Масоҳат"
    KALTMIETE = "💰 Kaltmiete"
    NEBENKOSTEN = "💸 Nebenkosten"
    START = "➡️ Кӯчидан мумкин аз"
    ENDE = "⬅️ Дастрас то"
    ANMELDUNG = "📝 Anmeldung"
    BESCHREIBUNG = "🧾 Шарҳи эълон"
    KONTAKT = "📞 Тамос"
    DIREKT_ANSCHREIBEN = "👉 Ба шахсӣ навиштан"
    STATUS = "Статус"
    STATUS_APPROVED = "Дар канал нашр шудааст"
    STATUS_PENDING = "Дар санҷиш"
    AD_CREATE_TIME = "Санаи эълон"

    SUBSCRIBE_INFO = "❗ Барои истифодаи бот, аввал бояд ба канал обуна шавед."
    SUBSCRIBE_TO_CHANNEL = "📢 Ба канал обуна шудан"
    SUBSCRIBED_TO_CHANNEL = "✅ Ман обуна шудам"

    THANKS_FOR_SUBSCRIPTION = "✅ Ташаккур! Акнун метавонед /new_ad истифода баред."
    STILL_NOT_SUBSCRIBED = "❌ Ҳоло ҳам обуна нестед. Лутфан ба канал обуна шавед."




class AdminText:
    NOT_ADMIN = "❌ Шумо админ нестед!"

    YOUR_AD_APPROVED = "✅ Эълони шумо тасдиқ шуд!\n🔗"
    YOUR_AD_REJECTED = "❌ Эълони шумо «{}» рад карда шуд."
    YOUR_AD_DELETED = "❌ Эълони шумо «{}» нест карда шуд."

    # PRESET_TEXT = "Hallo, ich schreibe Ihnen wegen Ihrer Anzeige:\n{}"


class MyAdsText:
    NO_ADS_YET = "📭 Шумо ҳоло эълон надоред."
    DELETE_MY_AD_BUTTON = "🗑 Нест кардан"
    ACTION = "⚙ Амал:"
    GET_AD_ERROR = "❌ Иҷозат нест ё эълон вуҷуд надорад."
    ERROR_DELETE_MY_AD = "❌ Хато ҳангоми нест кардани эълон."
    AD_DELETED = "✅ Эълон пурра нест карда шуд (аз канал ҳам)."


class NewAdText:
    SELECT_VERMIETUNG_ART = (
        "📝 Эълони нав додан.\n"
        "🏠 Намуди иҷораро интихоб кунед:"
    )

    VERMIETUNG_ART_WG = "🚪 Ҳуҷра (WG)"
    VERMIETUNG_ART_WOHNUNG = "🏢 Хона (Wohnung)"
    VERMIETUNG_ART_HAUS = "🏡 Ҳавли (Haus)"
    VERMIETUNG_ART_PARKPLATZ = "🅿 Ҷойи мошин"

    SELECTED_VERMIETUNG_ART = "✅ Намуди иҷора:"

    SELECT_AD_TYPE = "📢 Намуди эълонро интихоб кунед:"
    AD_TYPE_GESUCH = "🔴 Ҷустуҷӯ"
    AD_TYPE_ANGEBOT = "🟢 Пешниҳод"
    SELECTED_AD_TYPE = "✅ Намуди эълон:"

    INPUT_CITY = "🏙 Номи шаҳрро ворид кунед:"

    INPUT_KALTMIETE = "💶 Иҷораи холис (Kaltmiete €):"
    ERROR_INPUT_KALTMIETE = "❌ Воридот хато аст. Танҳо рақам ворид кунед."

    INPUT_NEBENKOSTEN = "💸 Хароҷоти иловагӣ (Nebenkosten €):"

    INPUT_RAUMFLAECHE = "📐 Масоҳат (м²)\n(Агар маълум набошад - ворид кунед):"

    SELECT_ANMELDUNG = "📝 Anmeldung мумкин аст?"
    ANMELDUNG_YES = "✅ Ҳа"
    ANMELDUNG_NO = "❌ Не"
    SELECTED_ANMELDUNG = "✅ Anmeldung мумкин:"

    INPUT_START_DATE = "📅 Аз кай?\n(Агар маълум набошад '-' ворид кунед)"
    INPUT_END_DATE = "📅 То кай?\n(Агар маълум набошад '-' ворид кунед)"

    INPUT_BESCHREIBUNG = "🧾 Шарҳи эълонро нависед (Beschreibung):"
    ERROR_BESCHREIBUNG = "❌ Шарҳ хеле кӯтоҳ аст (на камтар аз 5 ҳарф)."

    READY_ADD_PHOTO = (
        "✅ Ҳама маълумот ворид шуд!\n"
        "📷 Ихтиёрӣ: сурат фиристед\n"
        "➡️ Барои анҷом додан /finish-ро зер кунед."
    )
    ADDED_PHOTO = (
        "✅ Сурат илова шуд (ҳамагӣ {}).\n"
        "➡️ Барои анҷом додани эълон /finish-ро зер кунед."
    )
    ERROR_ADD_PHOTO = "❌ Акс ёфт нашуд. Бори дигар кӯшиш кунед."

    AD_SAVED = "✅ Эълон захира шуд! ⏳ Админ онро месанҷад."

    AD_LIMIT_REACHED = (
        "❌ Шумо ба ҳадди максималӣ {} эълонҳо расидед.\n\n"
        "🗑 Аввал як эълонро нест кунед."
    )
