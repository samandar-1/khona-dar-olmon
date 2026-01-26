import asyncio
# from khona_dar_olmon.db.database import init_db

# asyncio.run(init_db())
# print("✅ Alle Tabellen wurden erstellt!")
updates = context.bot.get_updates()
for u in updates:
    print(u.message.chat.id)
