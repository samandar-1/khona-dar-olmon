from db.database import AsyncSessionLocal
from sqlalchemy.future import select
from db.models import AdRequest, Ad

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

async def approve_ad_request(request_id: int):
    async with AsyncSessionLocal() as session:
        req = await session.get(AdRequest, request_id)
        if not req:
            return None

        req.status = "approved"

        if req.ad_id:
            ad = await session.get(Ad, req.ad_id)
            if ad:
                ad.approved = True

        await session.commit()
        return req

async def reject_ad_request(request_id: int):
    async with AsyncSessionLocal() as session:
        req = await session.get(AdRequest, request_id)
        if not req:
            return None

        req.status = "rejected"
        await session.commit()
        return req

async def get_pending():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(AdRequest).where(AdRequest.status == "pending")
        )
        return result.scalars().all()
