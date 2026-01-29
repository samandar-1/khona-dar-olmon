import json
from sqlalchemy import delete, select
from db.database import AsyncSessionLocal
from db.models import Ad, AdRequest


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
        return await session.get(Ad, ad_id)


# -------- GET USER ADS --------
async def get_user_ads(user_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Ad).where(Ad.user_id == user_id)
        )
        ads = result.scalars().all()
        return ads


# -------- DELETE AD --------
async def delete_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))
        await session.execute(delete(Ad).where(Ad.id == ad_id))
        await session.commit()
