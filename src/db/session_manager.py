from typing import Generator
from sqlalchemy.orm import Session
from src.db.connector import DbConnector

db_connector = DbConnector()


def get_db_session() -> Session:
    """
    Dependency that provides a SQLAlchemy session.

    Uses the DbConnector's get_db method to handle session lifecycle.
    The session is created for each request and closed after the request is done.
    """
    session = db_connector.get_db()
    try:
        yield session
    finally:
        session.close()
