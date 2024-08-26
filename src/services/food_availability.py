import logging
from sqlalchemy.orm import Session
from src.db.models.food_availability import FoodAvailability
from src.schemas.food_availability import FoodAvailabilityCreate, FoodAvailabilityUpdate
from src.exceptions import NotFoundException
from src.repositories.food_availability import FoodAvailabilityRepository

logger = logging.getLogger(__name__)


class FoodAvailabilityService:
    """
    Service class for handling business logic related to FoodAvailability.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.repository = FoodAvailabilityRepository(db_session)

    def get_food_availability(self, food_availability_id: int) -> FoodAvailability:
        """
        Retrieves a FoodAvailability object by its ID.
        """
        logger.info(f"Fetching FoodAvailability with ID {food_availability_id}.")
        food_availability = self.repository.get_food_availability(food_availability_id)
        if not food_availability:
            logger.error(f"FoodAvailability with ID {food_availability_id} not found.")
            raise NotFoundException(food_availability_id)
        return food_availability

    def create_food_availability(
        self, food_availability: FoodAvailabilityCreate
    ) -> FoodAvailability:
        """
        Creates a new FoodAvailability object.
        """
        logger.info("Creating new FoodAvailability entry.")
        return self.repository.create_food_availability(
            FoodAvailability(**food_availability.model_dump())
        )

    def update_food_availability(
        self,
        food_availability_id: int,
        food_availability_update: FoodAvailabilityUpdate,
    ) -> FoodAvailability:
        """
        Updates an existing FoodAvailability object.
        """
        logger.info(f"Updating FoodAvailability with ID {food_availability_id}.")
        food_availability = self.repository.get_food_availability(food_availability_id)
        if not food_availability:
            logger.error(f"FoodAvailability with ID {food_availability_id} not found.")
            raise NotFoundException(food_availability_id)

        return self.repository.update_food_availability(
            food_availability_id,
            food_availability_update.model_dump(exclude_unset=True),
        )

    def delete_food_availability(self, food_availability_id: int) -> FoodAvailability:
        """
        Deletes a FoodAvailability object by its ID.
        """
        logger.info(f"Deleting FoodAvailability with ID {food_availability_id}.")
        food_availability = self.repository.get_food_availability(food_availability_id)
        if not food_availability:
            logger.error(f"FoodAvailability with ID {food_availability_id} not found.")
            raise NotFoundException(food_availability_id)

        return self.repository.delete_food_availability(food_availability_id)
