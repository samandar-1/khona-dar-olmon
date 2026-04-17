from config.config import Config

if Config.LANGUAGE == "tj":
    from bot.strings_tj import *
elif Config.LANGUAGE == "uz":
    from bot.strings_uz import *
else:
    raise RuntimeError("Language not configured")