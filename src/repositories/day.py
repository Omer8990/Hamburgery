import logging
from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.day import Day
from src.schemas.day import DayCreate, DayUpdate
from src.db.connector import DbConnector
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class DayRepository:
    """
    Repository class for managing Day entities in the database.

    Provides methods for retrieving, creating, updating, and deleting Day records.
    """

    def __init__(self, db_connector: DbConnector):
        """
        Initializes the DayRepository with a DbConnector instance.

        :param db_connector: Instance of DbConnector for database operations.
        """
        self.db_connector = db_connector

    async def _get_day_by_id(self, day_id: int) -> Day:
        """
        Private helper method to retrieve a Day object by its ID.

        :param day_id: ID of the Day to retrieve.
        :return: Day object if found, else None.
        """
        async with self.db_connector.get_db() as db:
            query = select(Day).filter(Day.id == day_id)
            result = await db.execute(query)
            day = result.scalar_one_or_none()
            if not day:
                logger.warning(f"Day with ID {day_id} not found.")
            return day

    async def get_day(self, day_id: int) -> Day:
        """
        Retrieves a Day object by its ID.

        :param day_id: ID of the Day to retrieve.
        :return: Day object if found, else None.
        """
        logger.info(f"Fetching Day with ID {day_id}.")
        return await self._get_day_by_id(day_id)

    async def create_day(self, day: DayCreate) -> Day:
        """
        Creates a new Day object in the database.

        :param day: DayCreate schema with the data for the new Day.
        :return: The newly created Day object.
        """
        logger.info("Creating new Day entry.")
        async with self.db_connector.get_db() as db:
            db_day = Day(**day.model_dump())
            db.add(db_day)
            await db.refresh(db_day)
            logger.info(f"Day created with ID {db_day.id}.")
            return db_day

    async def update_day(self, day_id: int, day_update: DayUpdate) -> Day:
        """
        Updates an existing Day object in the database.

        :param day_id: ID of the Day to update.
        :param day_update: DayUpdate schema with the updated data.
        :return: The updated Day object.
        :raises NotFoundException: If the Day object is not found.
        """
        logger.info(f"Updating Day with ID {day_id}.")

        async with self.db_connector.get_db() as db:
            query = select(Day).filter(Day.id == day_id)
            result = await db.execute(query)
            db_day = result.scalar_one_or_none()

            if not db_day:
                logger.error(f"Update failed: Day with ID {day_id} not found.")
                raise NotFoundException(day_id)

            update_data = day_update.model_dump(exclude_unset=True)
            await db.execute(update(Day).where(Day.id == day_id).values(**update_data))
            await db.commit()

            updated_day = await self._get_day_by_id(day_id)
            logger.info(f"Day with ID {day_id} updated.")
            return updated_day

    async def delete_day(self, day_id: int) -> Day:
        """
        Deletes a Day object from the database by its ID.

        :param day_id: ID of the Day to delete.
        :return: The deleted Day object if it was found, else None.
        """
        logger.info(f"Deleting Day with ID {day_id}.")
        async with self.db_connector.get_db() as db:
            db_day = await self._get_day_by_id(day_id)
            if db_day:
                await db.delete(db_day)
                logger.info(f"Day with ID {day_id} deleted.")
            else:
                logger.warning(f"Delete failed: Day with ID {day_id} not found.")
            return db_day
