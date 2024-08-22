from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from src.config import settings

Base = declarative_base()


class DbConnector:
    """
    A class to manage the database connection and sessions.

    This class provides methods to get a session for database interactions,
    and to create or drop tables in the database.

    :param database_url: The database URL for connection. Defaults to settings.DATABASE_URL.
    """

    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.engine = create_async_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

    @asynccontextmanager
    async def get_db(
        self, auto_commit: bool = True
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides a database session within a context manager.

        :param auto_commit: If True, automatically commits the session. Defaults to True.
        :return: AsyncGenerator yielding an AsyncSession.
        """
        session: AsyncSession = self.SessionLocal()
        try:
            yield session
            if auto_commit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all_tables(self) -> None:
        """
        Creates all tables in the database based on the Base metadata.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all_tables(self) -> None:
        """
        Drops all tables in the database based on the Base metadata.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
