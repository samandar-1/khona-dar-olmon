from sqlalchemy.future import select
from db.database import AsyncSessionLocal
from db.models import User

async def get_or_create_user(telegram_id: str, username: str = None):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if user:
            return user

        user = User(
            telegram_id=telegram_id,
            username=username
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
