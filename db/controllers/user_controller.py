from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from db.database import AsyncSessionLocal
from db.models import User


async def save_or_update_user(telegram_user):
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.telegram_id == telegram_user.id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            user.username = telegram_user.username
            user.first_name = telegram_user.first_name
            user.last_name = telegram_user.last_name
        else:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name
            )
            session.add(user)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            stmt = select(User).where(User.telegram_id == telegram_user.id)
            result = await session.execute(stmt)
            user = result.scalars().first()

        return user



