from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.conversations.new_ad.handlers import *
from bot.conversations.new_ad.states import NewAdState


new_ad_conv = ConversationHandler(
    entry_points=[
        CommandHandler("new_ad", new_ad_start),
        CommandHandler("start", new_ad_start)
    ],

    states={
        NewAdState.VERMIETUNG_ART: [CallbackQueryHandler(new_ad_type_callback)],
        NewAdState.AD_TYPE: [CallbackQueryHandler(new_ad_type_callback2)],
        NewAdState.STADT: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_stadt)],
        NewAdState.KALTMIETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_kaltmiete)],
        NewAdState.NEBENKOSTEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_nebenkosten)],
        NewAdState.RAUMFLAECHE: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_raumflaeche)],
        NewAdState.ANMELDUNG: [CallbackQueryHandler(new_ad_anmeldung_callback)],
        NewAdState.START_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_start_date)],
        NewAdState.END_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_end_date)],
        NewAdState.TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_ad_title)],
        NewAdState.BILDER: [
            MessageHandler(filters.PHOTO, new_ad_bilder),
            CommandHandler("finish", new_ad_finish),
        ],
    },

    fallbacks=[CommandHandler("new_ad", new_ad_start)],
    allow_reentry=True,
)
