import json
from sqlalchemy import delete, select, func
from db.database import AsyncSessionLocal
from db.models import Ad, AdRequest, User
from sqlalchemy.orm import selectinload

# -------- CREATE AD --------
async def create_ad(**kwargs):
    async with AsyncSessionLocal() as session:
        ad = Ad(**kwargs)
        session.add(ad)
        await session.commit()
        await session.refresh(ad)
        return ad


# -------- GET AD --------
async def get_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad)
            .options(selectinload(Ad.user))
            .where(Ad.id == ad_id)
        )
        return result.scalar_one_or_none()


# -------- GET approved ads --------
async def get_approved_ads():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad)
            .options(selectinload(Ad.user))
            .where(Ad.approved == 1)
        )
        return result.scalars().all()


# -------- GET USER ADS --------
async def get_user_ads(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.user_id == user_id)
        )
        ads = result.scalars().all()
        return ads


async def count_user_ads(user_id: int) -> int:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count(Ad.id)).where(Ad.user_id == user_id)
        )
        return result.scalar() or 0

async def get_user_id_by_telegram(telegram_id: int) -> int | None:
    """
    Gibt die DB-ID eines Users anhand seiner Telegram-ID zurück.
    Falls der User nicht existiert, None.
    """
    async with AsyncSessionLocal() as session:
        stmt = select(User.id).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user_id = result.scalar_one_or_none()  # gibt direkt die ID oder None
        return user_id


# -------- DELETE AD --------
async def delete_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))
        await session.execute(delete(Ad).where(Ad.id == ad_id))
        await session.commit()
