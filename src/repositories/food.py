import logging
from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.food import Food
from src.schemas.food import FoodCreate, FoodUpdate
from src.db.connector import DbConnector
from src.exceptions import NotFoundException

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

    def _get_food_by_id(self, food_id: int) -> Food:
        """
        Private helper method to retrieve a Food object by its ID.

        :param food_id: ID of the Food to retrieve.
        :return: Food object if found, else None.
        """
        with self.db_connector.get_db() as db:
            query = select(Food).filter(Food.id == food_id)
            result = db.execute(query)
            food = result.scalar_one_or_none()
            if not food:
                logger.warning(f"Food with ID {food_id} not found.")
            return food

    def get_food(self, food_id: int) -> Food:
        """
        Retrieves a Food object by its ID.

        :param food_id: ID of the Food to retrieve.
        :return: Food object if found, else None.
        """
        logger.info(f"Fetching Food with ID {food_id}.")
        return self._get_food_by_id(food_id)

    def create_food(self, food: FoodCreate) -> Food:
        """
        Creates a new Food object in the database.

        :param food: FoodCreate schema with the data for the new Food.
        :return: The newly created Food object.
        """
        logger.info("Creating new Food entry.")
        with self.db_connector.get_db() as db:
            db_food = Food(**food.model_dump())
            db.add(db_food)
            db.refresh(db_food)
            logger.info(f"Food created with ID {db_food.id}.")
            return db_food

    def update_food(self, food_id: int, food_update: FoodUpdate) -> Food:
        """
        Updates an existing Food object in the database.

        :param food_id: ID of the Food to update.
        :param food_update: FoodUpdate schema with the updated data.
        :return: The updated Food object.
        :raises NotFoundException: If the Food object is not found.
        """
        logger.info(f"Updating Food with ID {food_id}.")

        with self.db_connector.get_db() as db:
            query = select(Food).filter(Food.id == food_id)
            result = db.execute(query)
            db_food = result.scalar_one_or_none()

            if not db_food:
                logger.error(f"Update failed: Food with ID {food_id} not found.")
                raise NotFoundException(food_id)

            update_data = food_update.model_dump(exclude_unset=True)
            db.execute(
                update(Food).where(Food.id == food_id).values(**update_data)
            )

            updated_food = self._get_food_by_id(food_id)
            logger.info(f"Food with ID {updated_food.id} updated.")
            return updated_food

    def delete_food(self, food_id: int) -> Food:
        """
        Deletes a Food object from the database by its ID.

        :param food_id: ID of the Food to delete.
        :return: The deleted Food object if it was found, else None.
        """
        logger.info(f"Deleting Food with ID {food_id}.")
        with self.db_connector.get_db() as db:
            db_food = self._get_food_by_id(food_id)
            if db_food:
                db.delete(db_food)
                logger.info(f"Food with ID {food_id} deleted.")
            else:
                logger.warning(f"Delete failed: Food with ID {food_id} not found.")
            return db_food
