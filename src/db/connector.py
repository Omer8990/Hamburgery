from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from contextlib import contextmanager

from src.config import settings

Base = declarative_base()


class DbConnector:
    """
    A class to manage the database connection and sessions.

    This class provides methods to get a session for database interactions,
    and to create or drop tables in the database.

    :param database_url: The database URL for connection.
    Defaults to settings.DATABASE_URL.
    """

    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._session: Session | None = None

    def _get_or_create_session(self) -> Session:
        """
        Creates a session if it doesn't exist,
        otherwise returns the existing session.
        """
        if self._session is None:
            self._session = self.SessionLocal()
        return self._session

    def close_session(self) -> None:
        """
        Closes the current session if it exists.
        """
        if self._session is not None:
            self._session.close()
            self._session = None

    @contextmanager
    def get_db(self, auto_commit: bool = True) -> Session:
        """
        Provides a database session within a context manager.

        :param auto_commit: If True, automatically commits the session. Defaults to True.
        :return: Generator yielding a Session.
        """
        session = self._get_or_create_session()
        try:
            yield session
            if auto_commit:
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.close_session()

    def create_all_tables(self) -> None:
        """
        Creates all tables in the database based on the Base metadata.
        """
        with self.engine.begin() as conn:
            Base.metadata.create_all(conn)

    def drop_all_tables(self) -> None:
        """
        Drops all tables in the database based on the Base metadata.
        """
        with self.engine.begin() as conn:
            Base.metadata.drop_all(conn)
