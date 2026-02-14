from db.database import AsyncSessionLocal
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import AdRequest, Ad
import json
async def create_ad_request(user_id: int, ad_id: int, action: str):
    async with AsyncSessionLocal() as session:
        req = AdRequest(
            user_id=user_id,
            ad_id=ad_id,
            action=action,      # "create" oder "update"
            status="pending"
        )

        session.add(req)
        await session.commit()
        await session.refresh(req)
        return req

# -------- APPROVE AD ----------
async def approve_ad(ad_id: int, telegram_msg_ids: list):
    async with AsyncSessionLocal() as session:
        ad = await session.get(Ad, ad_id)
        if not ad:
            return None

        ad.approved = True
        ad.telegram_message_id = json.dumps(telegram_msg_ids)

        await session.commit()
        return ad


# -------- REJECT AD ----------
async def reject_ad(ad_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(AdRequest).where(AdRequest.ad_id == ad_id))
        await session.execute(delete(Ad).where(Ad.id == ad_id))
        await session.commit()


async def get_pending():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AdRequest).where(AdRequest.status == "pending")
        )
        return result.scalars().all()
