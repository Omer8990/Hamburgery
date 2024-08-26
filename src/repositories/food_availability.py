import logging
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.db.models.food_availability import FoodAvailability

logger = logging.getLogger(__name__)


class FoodAvailabilityRepository:
    """
    Repository class for managing FoodAvailability entities in the database.

    Provides methods for retrieving, creating, updating, and deleting FoodAvailability records.
    """

    def __init__(self, db_session: Session):
        """
        Initializes the FoodAvailabilityRepository with a database session.

        :param db_session: SQLAlchemy Session for database operations.
        """
        self.db_session = db_session

    def get_food_availability_by_id(
        self, food_availability_id: int
    ) -> FoodAvailability:
        """
        Retrieves a FoodAvailability object by its ID.

        :param food_availability_id: ID of the FoodAvailability to retrieve.
        :return: FoodAvailability object if found, else None.
        """
        query = select(FoodAvailability).filter(
            FoodAvailability.id == food_availability_id
        )
        result = self.db_session.execute(query)
        return result.scalar_one_or_none()

    def create_food_availability(
        self, food_availability: FoodAvailability
    ) -> FoodAvailability:
        """
        Creates a new FoodAvailability object in the database.

        :param food_availability: FoodAvailability object to be added to the database.
        :return: The newly created FoodAvailability object.
        """
        self.db_session.add(food_availability)
        self.db_session.refresh(food_availability)
        return food_availability

    def update_food_availability(
        self, food_availability_id: int, update_data: dict
    ) -> None:
        """
        Updates an existing FoodAvailability object in the database.

        :param food_availability_id: ID of the FoodAvailability to update.
        :param update_data: Dictionary with the updated data.
        """
        self.db_session.execute(
            update(FoodAvailability)
            .where(FoodAvailability.id == food_availability_id)
            .values(**update_data)
        )

    def delete_food_availability(self, food_availability: FoodAvailability) -> None:
        """
        Deletes a FoodAvailability object from the database.

        :param food_availability: FoodAvailability object to delete.
        """
        self.db_session.delete(food_availability)
