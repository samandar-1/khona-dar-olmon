import logging
import sys


def setup_logging(language: str = ""):
    log_format = f"[%(asctime)s] [{language.upper()}] %(levelname)s %(name)s: %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )