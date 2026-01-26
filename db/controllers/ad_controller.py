from db.database import AsyncSessionLocal
from db.models import Ad, AdRequest
from sqlalchemy.future import select
from sqlalchemy import delete, select
async def create_ad(
    user_id: int,
    title: str,
    vermietung_art: str,
    type: str,
    kaltmiete: float | None,
    nebenkosten: float | None,
    raumflaeche: float | None,
    stadt: str,
    anmeldung_moeglich: bool,
    start_date,
    end_date,
    bilder: list[str],
    approved: bool = False,   # 🔥 HIER
):

    async with AsyncSessionLocal() as session:
        ad = Ad(
            user_id=user_id,
            title=title,
            vermietung_art=vermietung_art,
            type=type,
            kaltmiete=kaltmiete,
            nebenkosten=nebenkosten,
            raumflaeche=raumflaeche,
            stadt=stadt,
            anmeldung_moeglich=anmeldung_moeglich,
            start_date=start_date,
            end_date=end_date,
            bilder=bilder,
            approved=approved,
        )

        session.add(ad)
        await session.commit()
        await session.refresh(ad)
        return ad
async def update_ad(ad_id: int, user_id: int, **fields):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.id == ad_id, Ad.user_id == user_id)
        )
        ad = result.scalars().first()

        if not ad:
            return None

        for key, value in fields.items():
            if hasattr(ad, key):
                setattr(ad, key, value)

        ad.approved = False  # ❗ Änderung → erneut Admin-Freigabe
        await session.commit()
        await session.refresh(ad)
        return ad

async def delete_ad(ad_id: int, user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.id == ad_id, Ad.user_id == user_id)
        )
        ad = result.scalars().first()

        if not ad:
            return False

        await session.delete(ad)
        await session.commit()
        return True

async def get_user_ads(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.user_id == user_id)
        )
        return result.scalars().all()

async def get_ad_by_id(ad_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.id == ad_id)
        )
        return result.scalars().first()

# Anzeige freigeben
async def approve_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        # 1️⃣ Ad laden
        result = await session.execute(select(Ad).where(Ad.id == ad_id))
        ad = result.scalar_one_or_none()

        if not ad:
            return None  # optional: Fehlerhandling, falls Ad nicht gefunden

        # 2️⃣ Ad freigeben
        ad.approved = True
        session.add(ad)  # nicht zwingend nötig, aber sicherheitshalber

        # 3️⃣ Zugehörige AdRequests löschen
        await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))

        # 4️⃣ Änderungen speichern
        await session.commit()

        return ad

# Anzeige ablehnen
async def reject_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        # Anzeige löschen
        await session.execute(delete(Ad).where(Ad.id == ad_id))

        # Zugehörige AdRequests löschen
        await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))

        await session.commit()
