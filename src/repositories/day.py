import logging
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.db.models.day import Day
from src.schemas.day import DayCreate, DayUpdate
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class DayRepository:
    """
    Repository class for managing Day entities in the database.

    Provides methods for retrieving, creating, updating, and deleting Day records.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the DayRepository with a Session instance.

        :param db_session: SQLAlchemy Session instance for database operations.
        """
        self.db_session = db_session

    def _get_day_by_id(self, day_id: int) -> Day:
        """
        Private helper method to retrieve a Day object by its ID.

        :param day_id: ID of the Day to retrieve.
        :return: Day object if found, else None.
        """
        query = select(Day).filter(Day.id == day_id)
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def get_day(self, day_id: int) -> Day:
        """
        Retrieves a Day object by its ID.

        :param day_id: ID of the Day to retrieve.
        :return: Day object if found, else None.
        """
        logger.info(f"Fetching Day with ID {day_id}.")
        day = self._get_day_by_id(day_id)
        if not day:
            logger.warning(f"Day with ID {day_id} not found.")
        return day

    def create_day(self, day: DayCreate) -> Day:
        """
        Creates a new Day object in the database.

        :param day: DayCreate schema with the data for the new Day.
        :return: The newly created Day object.
        """
        logger.info("Creating new Day entry.")
        db_day = Day(**day.model_dump())
        self.db_session.add(db_day)
        logger.info(f"Day created with ID {db_day.id}.")
        return db_day

    def update_day(self, day_id: int, update_data: dict) -> Day:
        """
        Updates an existing Day object in the database.

        :param day_id: ID of the Day to update.
        :param update_data: Dictionary with updated data.
        :return: The updated Day object.
        :raises NotFoundException: If the Day object is not found.
        """
        logger.info(f"Updating Day with ID {day_id}.")

        db_day = self._get_day_by_id(day_id)
        if not db_day:
            logger.error(f"Update failed: Day with ID {day_id} not found.")
            raise NotFoundException(day_id)

        self.db_session.execute(
            update(Day).where(Day.id == day_id).values(**update_data)
        )

        updated_day = self._get_day_by_id(day_id)
        logger.info(f"Day with ID {day_id} updated.")
        return updated_day

    def delete_day(self, day_id: int) -> Day:
        """
        Deletes a Day object from the database by its ID.

        :param day_id: ID of the Day to delete.
        :return: The deleted Day object if it was found, else None.
        """
        logger.info(f"Deleting Day with ID {day_id}.")
        db_day = self._get_day_by_id(day_id)
        if db_day:
            self.db_session.delete(db_day)
            logger.info(f"Day with ID {day_id} deleted.")
        else:
            logger.warning(f"Delete failed: Day with ID {day_id} not found.")
        return db_day
