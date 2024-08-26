import logging
from src.repositories.food_availability import FoodAvailabilityRepository
from src.schemas.food_availability import FoodAvailabilityCreate, FoodAvailabilityUpdate
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class FoodAvailabilityService:
    """
    Service layer for managing FoodAvailability entities.

    This class provides business logic for creating, retrieving, updating, and deleting
    FoodAvailability records by interacting with the FoodAvailabilityRepository.
    """

    def __init__(self, food_availability_repository: FoodAvailabilityRepository):
        """
        Initializes the FoodAvailabilityService with a repository instance.

        :param food_availability_repository: Instance of FoodAvailabilityRepository.
        """
        self.food_availability_repository = food_availability_repository

    def get_food_availability(self, food_availability_id: int):
        """
        Retrieves a FoodAvailability entity by its ID.

        :param food_availability_id: ID of the FoodAvailability to retrieve.
        :return: The FoodAvailability object if found.
        :raises NotFoundException: If no FoodAvailability with the given ID exists.
        """
        logger.info(f"Fetching FoodAvailability with ID {food_availability_id}.")
        food_availability = (
            self.food_availability_repository.get_food_availability_by_id(
                food_availability_id
            )
        )
        if not food_availability:
            logger.warning(
                f"FoodAvailability with ID {food_availability_id} not found."
            )
            raise NotFoundException(
                f"FoodAvailability with ID {food_availability_id} not found."
            )
        logger.info(
            f"FoodAvailability with ID {food_availability_id} retrieved successfully."
        )
        return food_availability

    def create_food_availability(self, food_availability: FoodAvailabilityCreate):
        """
        Creates a new FoodAvailability entity.

        :param food_availability: Data required to create a new FoodAvailability.
        :return: The newly created FoodAvailability object.
        """
        logger.info("Creating new FoodAvailability entry.")
        created_food_availability = (
            self.food_availability_repository.create_food_availability(
                food_availability
            )
        )
        logger.info(f"FoodAvailability created with ID {created_food_availability.id}.")
        return created_food_availability

    def update_food_availability(
        self,
        food_availability_id: int,
        food_availability_update: FoodAvailabilityUpdate,
    ):
        """
        Updates an existing FoodAvailability entity.

        :param food_availability_id: ID of the FoodAvailability to update.
        :param food_availability_update: Data for updating the FoodAvailability.
        :return: The updated FoodAvailability object.
        :raises NotFoundException: If no FoodAvailability with the given ID exists.
        """
        logger.info(f"Updating FoodAvailability with ID {food_availability_id}.")
        self.get_food_availability(
            food_availability_id
        )  # This ensures the entity exists

        update_data = food_availability_update.model_dump(exclude_unset=True)
        updated_food_availability = (
            self.food_availability_repository.update_food_availability(
                food_availability_id, update_data
            )
        )
        logger.info(
            f"FoodAvailability with ID {food_availability_id} updated successfully."
        )
        return updated_food_availability

    def delete_food_availability(self, food_availability_id: int):
        """
        Deletes a FoodAvailability entity by its ID.

        :param food_availability_id: ID of the FoodAvailability to delete.
        :return: The deleted FoodAvailability object.
        :raises NotFoundException: If no FoodAvailability with the given ID exists.
        """
        logger.info(f"Deleting FoodAvailability with ID {food_availability_id}.")
        food_availability = self.get_food_availability(
            food_availability_id
        )  # Ensures the entity exists
        self.food_availability_repository.delete_food_availability(food_availability)
        logger.info(
            f"FoodAvailability with ID {food_availability_id} deleted successfully."
        )
        return food_availability
