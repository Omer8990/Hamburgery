import logging
from src.repositories.food import FoodRepository
from src.schemas.food import FoodCreate, FoodUpdate
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class FoodService:
    """
    Service class for managing Food entities.

    Provides methods for retrieving, creating, updating, and deleting Food records.
    """

    def __init__(self, food_repository: FoodRepository):
        """
        Initializes the FoodService with a FoodRepository instance.

        :param food_repository: FoodRepository instance for interacting with the database.
        """
        self.food_repository = food_repository

    def get_food(self, food_id: int):
        """
        Retrieves a Food object by its ID.

        :param food_id: ID of the Food to retrieve.
        :return: Food object if found, else None.
        :raises NotFoundException: If the Food object is not found.
        """
        logger.info(f"Fetching Food with ID {food_id}.")
        food = self.food_repository._get_food_by_id(food_id)
        if not food:
            logger.error(f"Food with ID {food_id} not found.")
            raise NotFoundException(f"Food with ID {food_id} not found.")
        return food

    def create_food(self, food: FoodCreate):
        """
        Creates a new Food object in the database.

        :param food: FoodCreate schema with the data for the new Food.
        :return: The newly created Food object.
        """
        logger.info("Creating new Food entry.")
        new_food = self.food_repository.create_food(food)
        logger.info(f"Food created with ID {new_food.id}.")
        return new_food

    def update_food(self, food_id: int, food_update: FoodUpdate):
        """
        Updates an existing Food object in the database.

        :param food_id: ID of the Food to update.
        :param food_update: FoodUpdate schema with the updated data.
        :return: The updated Food object.
        :raises NotFoundException: If the Food object is not found.
        """
        logger.info(f"Updating Food with ID {food_id}.")
        self.get_food(food_id)

        updated_food = self.food_repository.update_food(food_id, food_update)
        logger.info(f"Food with ID {updated_food.id} updated.")
        return updated_food

    def delete_food(self, food_id: int):
        """
        Deletes a Food object from the database by its ID.

        :param food_id: ID of the Food to delete.
        :return: The deleted Food object if it was found, else None.
        :raises NotFoundException: If the Food object is not found.
        """
        logger.info(f"Deleting Food with ID {food_id}.")
        food = self.get_food(food_id)
        self.food_repository.delete_food(food_id)
        logger.info(f"Food with ID {food_id} deleted.")
        return food
