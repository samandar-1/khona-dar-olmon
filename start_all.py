import multiprocessing
from config.config import load_config


def run_tj():
    load_config("config/config_tj.env")

    from bot.main import run
    run()


def run_uz():
    load_config("config/config_uz.env")

    from bot.main import run
    run()


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_tj)
    p2 = multiprocessing.Process(target=run_uz)

    p1.start()
    p2.start()

    p1.join()
    p2.join()