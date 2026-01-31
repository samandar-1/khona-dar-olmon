from enum import Enum, auto


MAX_ADS_PER_USER = 3


class NewAdState(Enum):
    TITLE = auto()
    VERMIETUNG_ART = auto()
    AD_TYPE = auto()
    KALTMIETE = auto()
    NEBENKOSTEN = auto()
    RAUMFLAECHE = auto()
    STADT = auto()
    ANMELDUNG = auto()
    START_DATE = auto()
    END_DATE = auto()
    BILDER = auto()
    CONFIRM = auto()

