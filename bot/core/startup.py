from db.database import init_db, init_engine
from bot.core.commands import set_commands
from config.config import Config

async def on_startup(app):
    init_engine()
    await init_db()

    # if AsyncSessionLocal is None:
    #     raise RuntimeError("SessionLocal ist None")

    await set_commands(app)

    print(f"✅ Startup abgeschlossen | DB: {Config.DB_PATH}")
