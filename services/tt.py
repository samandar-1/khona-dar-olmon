import asyncio
from khona_dar_olmon.db.database import create_db

asyncio.run(create_db())
print("✅ Alle Tabellen wurden erstellt!")

