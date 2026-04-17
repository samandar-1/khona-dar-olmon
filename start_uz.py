from config.config import load_config
load_config("config/config_uz.env")

from bot.main import run

if __name__ == "__main__":
    run()