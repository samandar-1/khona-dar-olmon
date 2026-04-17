import multiprocessing
import os


def run_tj():
    os.environ["ENV_FILE"] = "config/config_tj.env"

    from config.config import load_config
    load_config("config/config_tj.env")  # ← erst Config laden

    from bot.main import run  # ← dann importieren
    run()


def run_uz():
    os.environ["ENV_FILE"] = "config/config_uz.env"

    from config.config import load_config
    load_config("config/config_uz.env")  # ← erst Config laden

    from bot.main import run  # ← dann importieren
    run()


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_tj)
    p2 = multiprocessing.Process(target=run_uz)
    p1.start()
    p2.start()
    p1.join()
    p2.join()