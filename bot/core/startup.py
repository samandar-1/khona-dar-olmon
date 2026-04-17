from db.database import init_db, init_engine
from bot.core.commands import set_commands
from config.config import Config
import logging

logger = logging.getLogger(__name__)

async def on_startup(app):
    init_engine()
    await init_db()
    await set_commands(app)
    logger.info("Startup abgeschlossen | DB: %s | Language: %s", Config.DB_PATH, Config.LANGUAGE)