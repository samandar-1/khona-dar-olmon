from db.database import init_db
from bot.core.commands import set_commands

async def on_startup(app):
    await init_db()
    await set_commands(app)
    print("✅ Startup abgeschlossen (DB + Commands)")
