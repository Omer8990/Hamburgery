import logging
from sqlalchemy.future import select
from sqlalchemy import update
from src.db.models.food_availability import FoodAvailability
from src.schemas.food_availability import FoodAvailabilityCreate, FoodAvailabilityUpdate
from src.db.connector import DbConnector
from src.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class FoodAvailabilityRepository:
    """
    Repository class for managing FoodAvailability entities in the database.

    Provides methods for retrieving, creating, updating, and deleting FoodAvailability records.
    """

    def __init__(self, db_connector: DbConnector):
        """
        Initializes the FoodAvailabilityRepository with a DbConnector instance.

        :param db_connector: Instance of DbConnector for database operations.
        """
        self.db_connector = db_connector

    def _get_food_availability_by_id(
        self, food_availability_id: int
    ) -> FoodAvailability:
        """
        Private helper method to retrieve a FoodAvailability object by its ID.

        :param food_availability_id: ID of the FoodAvailability to retrieve.
        :return: FoodAvailability object if found, else None.
        """
        with self.db_connector.get_db() as db:
            query = select(FoodAvailability).filter(
                FoodAvailability.id == food_availability_id
            )
            result = db.execute(query)
            food_availability = result.scalar_one_or_none()
            if not food_availability:
                logger.warning(
                    f"FoodAvailability with ID {food_availability_id} not found."
                )
            return food_availability

    def get_food_availability(
        self, food_availability_id: int
    ) -> FoodAvailability:
        """
        Retrieves a FoodAvailability object by its ID.

        :param food_availability_id: ID of the FoodAvailability to retrieve.
        :return: FoodAvailability object if found, else None.
        """
        logger.info(f"Fetching FoodAvailability with ID {food_availability_id}.")
        return self._get_food_availability_by_id(food_availability_id)

    def create_food_availability(
        self, food_availability: FoodAvailabilityCreate
    ) -> FoodAvailability:
        """
        Creates a new FoodAvailability object in the database.

        :param food_availability: FoodAvailabilityCreate schema with the data for the new FoodAvailability.
        :return: The newly created FoodAvailability object.
        """
        logger.info("Creating new FoodAvailability entry.")
        with self.db_connector.get_db() as db:
            db_food_availability = FoodAvailability(**food_availability.model_dump())
            db.add(db_food_availability)
            db.refresh(db_food_availability)
            logger.info(f"FoodAvailability created with ID {db_food_availability.id}.")
            return db_food_availability

    def update_food_availability(
        self,
        food_availability_id: int,
        food_availability_update: FoodAvailabilityUpdate,
    ) -> FoodAvailability:
        """
        Updates an existing FoodAvailability object in the database.

        :param food_availability_id: ID of the FoodAvailability to update.
        :param food_availability_update: FoodAvailabilityUpdate schema with the updated data.
        :return: The updated FoodAvailability object.
        :raises NotFoundException: If the FoodAvailability object is not found.
        """
        logger.info(f"Updating FoodAvailability with ID {food_availability_id}.")

        with self.db_connector.get_db() as db:
            query = select(FoodAvailability).filter(
                FoodAvailability.id == food_availability_id
            )
            result = db.execute(query)
            db_food_availability = result.scalar_one_or_none()

            if not db_food_availability:
                logger.error(
                    f"Update failed: FoodAvailability with ID {food_availability_id} not found."
                )
                raise NotFoundException(food_availability_id)

            update_data = food_availability_update.model_dump(exclude_unset=True)
            db.execute(
                update(FoodAvailability)
                .where(FoodAvailability.id == food_availability_id)
                .values(**update_data)
            )

            updated_food_availability = self._get_food_availability_by_id(
                food_availability_id
            )
            logger.info(
                f"FoodAvailability with ID {updated_food_availability.id} updated."
            )
            return updated_food_availability

    def delete_food_availability(
        self, food_availability_id: int
    ) -> FoodAvailability:
        """
        Deletes a FoodAvailability object from the database by its ID.

        :param food_availability_id: ID of the FoodAvailability to delete.
        :return: The deleted FoodAvailability object if it was found, else None.
        """
        logger.info(f"Deleting FoodAvailability with ID {food_availability_id}.")
        with self.db_connector.get_db() as db:
            db_food_availability = self._get_food_availability_by_id(
                food_availability_id
            )
            if db_food_availability:
                db.delete(db_food_availability)
                logger.info(f"FoodAvailability with ID {food_availability_id} deleted.")
            else:
                logger.warning(
                    f"Delete failed: FoodAvailability with ID {food_availability_id} not found."
                )
            return db_food_availability
