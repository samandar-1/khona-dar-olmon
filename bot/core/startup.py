from db.database import init_db

async def on_startup(app):
    await init_db()
    print("DB ready")
