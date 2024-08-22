import logging
from sqlalchemy.future import select
from src.db.models.food import Food
from src.schemas.food import FoodCreate, FoodUpdate
from src.db.connector import DbConnector
from src.exceptions import FoodNotFoundException

logger = logging.getLogger(__name__)


class FoodRepository:
    """
    Repository class for managing Food entities in the database.

    Provides methods for retrieving, creating, updating, and deleting Food records.
    """

    def __init__(self, db_connector: DbConnector):
        """
        Initializes the FoodRepository with a DbConnector instance.

        :param db_connector: Instance of DbConnector for database operations.
        """
        self.db_connector = db_connector

    async def _get_food_by_id(self, food_id: int) -> Food:
        """
        Private helper method to retrieve a Food object by its ID.

        :param food_id: ID of the Food to retrieve.
        :return: Food object if found, else None.
        """
        async with self.db_connector.get_db() as db:
            query = select(Food).filter(Food.id == food_id)
            result = await db.execute(query)
            food = result.scalar_one_or_none()
            if not food:
                logger.warning(f"Food with ID {food_id} not found.")
            return food

    async def get_food(self, food_id: int) -> Food:
        """
        Retrieves a Food object by its ID.

        :param food_id: ID of the Food to retrieve.
        :return: Food object if found, else None.
        """
        logger.info(f"Fetching Food with ID {food_id}.")
        return await self._get_food_by_id(food_id)

    async def create_food(self, food: FoodCreate) -> Food:
        """
        Creates a new Food object in the database.

        :param food: FoodCreate schema with the data for the new Food.
        :return: The newly created Food object.
        """
        logger.info("Creating new Food entry.")
        async with self.db_connector.get_db() as db:
            db_food = Food(**food.model_dump())
            db.add(db_food)
            await db.refresh(db_food)
            logger.info(f"Food created with ID {db_food.id}.")
            return db_food

    async def update_food(self, food_id: int, food_update: FoodUpdate) -> Food:
        """
        Updates an existing Food object in the database.

        :param food_id: ID of the Food to update.
        :param food_update: FoodUpdate schema with the updated data.
        :return: The updated Food object.
        :raises FoodNotFoundException: If the Food object is not found.
        """
        logger.info(f"Updating Food with ID {food_id}.")
        async with self.db_connector.get_db() as db:
            db_food = await self._get_food_by_id(food_id)
            if not db_food:
                logger.error(f"Update failed: Food with ID {food_id} not found.")
                raise FoodNotFoundException(food_id)

            for key, value in food_update.model_dump(exclude_unset=True).items():
                setattr(db_food, key, value)
            await db.refresh(db_food)
            logger.info(f"Food with ID {db_food.id} updated.")
            return db_food

    async def delete_food(self, food_id: int) -> Food:
        """
        Deletes a Food object from the database by its ID.

        :param food_id: ID of the Food to delete.
        :return: The deleted Food object if it was found, else None.
        """
        logger.info(f"Deleting Food with ID {food_id}.")
        async with self.db_connector.get_db() as db:
            db_food = await self._get_food_by_id(food_id)
            if db_food:
                await db.delete(db_food)
                logger.info(f"Food with ID {food_id} deleted.")
            else:
                logger.warning(f"Delete failed: Food with ID {food_id} not found.")
            return db_food
