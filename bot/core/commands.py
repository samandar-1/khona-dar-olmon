from telegram import BotCommand

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("new_ad", "Neue Anzeige"),
        BotCommand("show_my_ads", "Meine Anzeigen"),
        BotCommand("admin_ads", "Admin Check"),
    ])
