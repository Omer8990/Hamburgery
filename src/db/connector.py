from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config import settings  # Assuming you have a settings module for configuration

Base = declarative_base()

class DbConnector:
    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.engine = create_async_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session

    async def create_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
