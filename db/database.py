from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Base
from config.config import Config

engine = None
AsyncSessionLocal = None


def init_engine():
    global engine, AsyncSessionLocal

    if not Config.DB_PATH:
        raise RuntimeError("DB_PATH not set")

    DATABASE_URL = f"sqlite+aiosqlite:///{Config.DB_PATH}"

    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        future=True
    )

    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


def get_session():
    if AsyncSessionLocal is None:
        raise RuntimeError("DB nicht initialisiert. init_engine() wurde nicht aufgerufen.")

    return AsyncSessionLocal()

async def init_db():
    global engine

    if engine is None:
        init_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)