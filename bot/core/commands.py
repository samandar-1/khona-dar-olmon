from telegram import BotCommand
from bot.strings import GeneralText

async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("new_ad", GeneralText.COMMAND_NEW_AD),
        BotCommand("show_my_ads", GeneralText.COMMAND_SHOW_MY_ADS),
        # BotCommand("admin_ads", GeneralText.COMMAND_ADMIN_ADS),
    ])

