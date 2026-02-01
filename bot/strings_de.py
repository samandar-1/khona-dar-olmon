class GeneralText:
    COMMAND_NEW_AD = "➕ Neue Anzeige"
    COMMAND_SHOW_MY_ADS = "📋 Meine Anzeigen"
    COMMAND_ADMIN_ADS = "🛠 Admin-Check"

    # Allgemeine Anzeigen-Labels
    UNKNOWN = "❓ Unbekannt"
    STADT = "📍 Stadt"
    FLAECHE = "📐 Fläche"
    KALTMIETE = "💰 Kaltmiete"
    NEBENKOSTEN = "💸 Nebenkosten"
    START = "➡️ Start"
    ENDE = "⬅️ Ende"
    ANMELDUNG = "📝 Anmeldung"
    BESCHREIBUNG = "🧾 Beschreibung"
    KONTAKT = "📞 Kontakt"
    DIREKT_ANSCHREIBEN = "👉 Direkt anschreiben"
    STATUS = "Status"
    STATUS_APPROVED = "Im Kanal veröffentlicht"
    STATUS_PENDING = "In Prüfung"

class AdminText:
    NOT_ADMIN = "❌ Du bist kein Admin!"

    YOUR_AD_APPROVED = "✅ Deine Anzeige wurde freigegeben!\n🔗"
    YOUR_AD_REJECTED = "❌ Deine Anzeige „{}“ wurde abgelehnt."

class MyAdsText:
    NO_ADS_YET = "📭 Du hast noch keine Anzeigen."
    DELETE_MY_AD_BUTTON = "🗑 Löschen"
    ACTION = "⚙ Aktion:"
    GET_AD_ERROR = "❌ Keine Berechtigung oder Anzeige existiert nicht."
    ERROR_DELETE_MY_AD = "❌ Fehler beim Löschen der Anzeige."
    AD_DELETED = "✅ Anzeige wurde vollständig gelöscht (inkl. Kanal)."



class NewAdText:
    SELECT_VERMIETUNG_ART = (
        "📝 Neue Anzeige erstellen\n"
        "🏠 Bitte wähle die Art der Vermietung:"
    )

    VERMIETUNG_ART_WG = "🏘 WG"
    VERMIETUNG_ART_WOHNUNG = "🏢 Wohnung"
    VERMIETUNG_ART_HAUS = "🏡 Haus"
    VERMIETUNG_ART_PARKPLATZ = "🅿 Parkplatz"

    SELECTED_VERMIETUNG_ART = "✅ Vermietungsart:"

    SELECT_AD_TYPE = "📢 Bitte wähle den Typ der Anzeige:"
    AD_TYPE_GESUCH = "🔍 Gesuch"
    AD_TYPE_ANGEBOT = "📢 Angebot"
    SELECTED_AD_TYPE = "✅ Anzeige-Typ:"

    INPUT_CITY = "🏙 Bitte gib die Stadt ein:"

    INPUT_KALTMIETE = "💶 Bitte gib die Kaltmiete in Euro ein:"
    ERROR_INPUT_KALTMIETE = "❌ Ungültige Eingabe. Bitte nur Zahlen verwenden."

    INPUT_NEBENKOSTEN = "💸 Bitte gib die Nebenkosten in Euro ein:"

    INPUT_RAUMFLAECHE = "📐 Bitte gib die Fläche in m² ein:"

    SELECT_ANMELDUNG = "📝 Anmeldung möglich?"
    ANMELDUNG_YES = "✅ Ja"
    ANMELDUNG_NO = "❌ Nein"
    SELECTED_ANMELDUNG = "✅ Anmeldung möglich:"

    INPUT_START_DATE = "📅 Ab wann? (optional)"
    INPUT_END_DATE = "📅 Bis wann? (optional)"

    INPUT_BESCHREIBUNG = "🧾 Bitte gib eine Beschreibung für deine Anzeige ein:"
    ERROR_BESCHREIBUNG = "❌ Beschreibung zu kurz (mindestens 5 Zeichen)."

    READY_ADD_PHOTO = (
        "✅ Alle Daten erfasst!\n"
        "📷 Optional: Sende jetzt Bilder oder gib /finish ein, um die Anzeige zu speichern."
    )
    ADDED_PHOTO = (
        "✅ Bild hinzugefügt ({} insgesamt).\n"
        "➡️ Gib /finish ein, um die Anzeige zu speichern."
    )
    ERROR_ADD_PHOTO = "❌ Kein Bild erkannt. Bitte versuche es erneut."

    AD_SAVED = "✅ Anzeige gespeichert! ⏳ Sie wird nun vom Admin geprüft."

    AD_LIMIT_REACHED = (
            "❌ Du hast bereits das maximale Limit von "
            "{} Anzeigen erreicht.\n\n"
            "🗑 Bitte lösche zuerst eine Anzeige, um eine neue zu erstellen."
        )
