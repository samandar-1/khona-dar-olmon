import os
from dotenv import load_dotenv


class Config:
    BOT_TOKEN = None
    ADMIN_IDS = None
    DB_PATH = None
    CHANNEL_USERNAME = None
    CHANNEL_ID = None
    LANGUAGE = None


def load_config(env_file):
    load_dotenv(env_file, override=True)

    Config.BOT_TOKEN = os.getenv("BOT_TOKEN")
    Config.ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x] # deine Telegram-User-ID(s)
    Config.DB_PATH = os.getenv("DB_PATH")
    Config.CHANNEL_USERNAME = str(os.getenv("CHANNEL_USERNAME"))
    Config.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
    Config.LANGUAGE = os.getenv("LANGUAGE")